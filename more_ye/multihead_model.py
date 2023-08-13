import torch
import torch.nn as nn
import math
from torch.nn import functional as F


class SelfAttention(nn.Module):
    def __init__(self,n_embd,heads,dropout):
        super(SelfAttention,self).__init__()
        self.heads = heads
        self.n_embd = n_embd
        self.dropout = nn.Dropout(dropout)
        self.query = nn.Linear(n_embd,n_embd,bias=False)
        self.key = nn.Linear(n_embd,n_embd,bias=False)
        self.value = nn.Linear(n_embd,n_embd,bias=False)
        self.c_proj = nn.Linear(n_embd,n_embd,bias=False)
        assert n_embd % heads == 0
    def forward(self,query,key,value,mask):
        B,T,C = query.size()
        query = self.query(query).view(B, T ,self.heads, self.n_embd//self.heads).transpose(1,2)
        key = self.key(key).view(B, T, self.heads, self.n_embd//self.heads).transpose(1,2)
        value = self.value(value).view(B, T, self.heads, self.n_embd//self.heads).transpose(1,2)
        att = (query @ key.transpose(-2,-1)) * (1.0 / math.sqrt(key.size(-1)))
        if mask is not None:
            att = att.masked_fill(mask[:,:,:T,:T] == 0,float(-1e12))
        att = F.softmax(att,dim=-1)
        att = self.dropout(att)
        y = att @ value
        y = y.transpose(1,2).contiguous().view(B,T,C)
        y = self.dropout(self.c_proj(y))
        return y
class MLP(nn.Module):
    def __init__(self,n_embd,fwd_exp,dropout):
        super().__init__()
        self.ff = nn.Linear(n_embd,n_embd*fwd_exp,bias=False)
        self.gelu = nn.GELU()
        self.ff_proj = nn.Linear(fwd_exp*n_embd,n_embd,bias=False)
        self.dropout = nn.Dropout(dropout)
    def forward(self,x):
        x = self.ff(x)
        x = self.gelu(x)
        x = self.ff_proj(x)
        x = self.dropout(x)
        return x

class TransformerBlock(nn.Module):
    def __init__(self,n_embd,heads,dropout,fwd_exp):
        super(TransformerBlock,self).__init__()
        self.attention = SelfAttention(n_embd,heads,dropout)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)
        self.mlp = MLP(n_embd,fwd_exp,dropout)
        self.dropout = nn.Dropout(dropout)
    def forward(self,query,key,value,mask):
        x = query + self.attention(self.ln1(query),self.ln1(key),self.ln1(value),mask)
        x = x + self.mlp(self.ln2(x))
        return x
class Encoder(nn.Module):
    def __init__(self,src_vocab_sz,n_embd,layers,heads,device,fwd_exp,dropout,block_sz):
        super(Encoder,self).__init__()
        self.n_embd = n_embd
        self.device = device
        self.block_sz = block_sz
        self.dropout = nn.Dropout(dropout)
        self.wbe = nn.Embedding(src_vocab_sz,n_embd)
        self.pse =nn.Embedding(block_sz,n_embd)
        self.layers = nn.ModuleList([TransformerBlock(n_embd,heads,dropout=dropout,fwd_exp=fwd_exp) for _ in range(layers)])

    def forward(self,x,mask):
        device = x.device
        b,t = x.size()
        assert t <= self.block_sz
        pos = torch.arange(0,t,dtype=torch.long,device=device)
        out = self.dropout(self.wbe(x) + self.pse(pos))
        for layer in self.layers:
            out = layer(out,out,out,mask)
        return out
class DecoderBlock(nn.Module):
    def __init__(self,n_embd,heads,fwd_exp,dropout,device):
        super(DecoderBlock,self).__init__()
        self.device = device
        self.n_embd = n_embd
        self.ln = nn.LayerNorm(n_embd)
        self.dropout = nn.Dropout(dropout)
        self.attention = SelfAttention(n_embd,heads,dropout)
        self.transformer_block = TransformerBlock(n_embd,heads,dropout,fwd_exp)
    def forward(self,x,enc_out,src_mask,tgt_mask):
        attention = self.attention(x,x,x,tgt_mask)
        query = self.dropout(self.ln(attention + x))
        out = self.transformer_block(query,enc_out,enc_out,src_mask)
        return out
class Decoder(nn.Module):
    def __init__(self,tgt_vocab_sz,n_embd,layers,heads,fwd_exp,dropout,device,block_sz):
        super(Decoder,self).__init__()
        self.device = device 
        self.wbe = nn.Embedding(tgt_vocab_sz,n_embd)
        self.pse = nn.Embedding(block_sz,n_embd)
        self.layers = nn.ModuleList([DecoderBlock(n_embd,heads,fwd_exp,dropout,device) for _ in range(layers)])
        self.c_proj = nn.Linear(n_embd,tgt_vocab_sz)
        self.dropout = nn.Dropout(dropout)
    def forward(self,x,enc_out,src_mask,tgt_mask):
        device = x.device
        b,t = x.size()
        pos = torch.arange(0,t,dtype=torch.long,device=device)
        out = self.dropout(self.wbe(x) + self.pse(pos))
        for layer in self.layers:
            out = layer(out,enc_out,src_mask,tgt_mask)
        out = self.c_proj(out)
        return out
class Transformer(nn.Module):
    def __init__(self,src_vocab_sz,tgt_vocab_sz,src_pad_idx,tgt_pad_idx,n_embd=256,layers=6,fwd_exp=4,heads=8,dropout=0,device="cuda",block_sz = 100):
        super(Transformer,self).__init__()
        self.encoder = Encoder(src_vocab_sz,n_embd,layers,heads,device,fwd_exp,dropout,block_sz)
        self.decoder = Decoder(tgt_vocab_sz,n_embd,layers,heads,fwd_exp,dropout,device,block_sz)
        self.src_pad_idx = src_pad_idx
        self.tgt_pad_idx = tgt_pad_idx
        self.device = device
    
    def get_num_params(self,non_embedding=True):
        n_params = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n_params -= self.Transformer.wpe.weight.numel()
        return n_params

    def make_src_mask(self,src):
        src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
        return src_mask.to(self.device)
    def make_tgt_mask(self,tgt):
        n,t = tgt.shape
        tgt_mask = torch.tril(torch.ones(t,t)).view(1,1,t,t)
        return tgt_mask.to(self.device)
    def forward(self,src,tgt):
        src_mask = self.make_src_mask(src)
        tgt_mask = self.make_tgt_mask(tgt)
        enc_src = self.encoder(src,src_mask)
        out = self.decoder(tgt,enc_src,src_mask,tgt_mask)
        return out
if __name__ =="__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    B,T,C = 4,8,32
    x = torch.randint(0,10,size=(B,T),device=device)
    tgt =  torch.randint(0,10,size=(B,T),device=device)
    src_pad_idx = 0
    tgt_pad_idx = 0
    src_vocab_size = 10
    tgt_vocab_size = 10
    model = Transformer(src_vocab_size,tgt_vocab_size,src_pad_idx,tgt_pad_idx).to(device)
    out = model(x,tgt)
    print(out.shape)