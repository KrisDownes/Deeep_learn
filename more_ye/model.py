import math
import torch
import torch.nn as nn
from torch.nn import functional as F

n_dim = 512
n_heads = 8
head_size = n_dim//n_heads

class EncoderDecoder(nn.Module):
    def __init__(self,encoder,decoder,src_embd,tgt_embd,generator):
        super(EncoderDecoder,self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embd = src_embd
        self.tgt_embd = tgt_embd
        self.generator = generator
    def forward(self,src,tgt,src_mask,tgt_mask):
        return self.decode(self.encode(src,src_mask),src_mask,tgt,tgt_mask)
    def encode(self,src,src_mask):
        return self.encoder(self.src_embd(src),src_mask)
    def decode(self,memory,src_mask,tgt,tgt_mask):
        return self.decoder(self.tgt_embd(tgt),memory,src_mask,tgt_mask)

class Generator(nn.Module):
    def __init__(self,d_model,vocab):
        super(Generator,self).__init__()
        self.proj = nn.Linear(d_model,vocab)

    def forward(self,x):
        return F.log_softmax(self.proj(x),dim=1)

class Encoder(nn.Module):
    "Stack of N layer encoders"
    def __init__(self,layer,N):
        super(Encoder,self).__init__()
        self.norm = LayerNorm(layer.size)
        self.layers = nn.ModuleList([layer for _ in range(N)])

    def forward(self,x,mask):
        for layer in self.layers:
            x = layer(x,mask)
        return self.norm(x)
    
class LayerNorm(nn.Module):
    def __init__(self,features,eps=1e-6):
        super(LayerNorm,self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self,x):
        mean = x.mean(-1,keepdim=True)
        std = x.std(-1,keepdim=True)
        return self.a_2 * (x-mean) / (std + self.eps) + self.b_2
    
class EncoderLayer(nn.Module):
    "Encoder Layer is made up of LayerNorm,self-Attention and MLP"
    def __init__(self,size,self_attn,MLP,dropout):
        super(EncoderLayer,self).__init__()
        self.self_attn = self_attn
        self.MLP = MLP
        self.size = size
    def forward(self,x,mask):
        "Encoder Layer from paper with LayerNorm before connections"



def attention(query,key,value,mask = None,dropout=None):
    d_k = query.size(-1)
    scores = (query @ key.transpose(-2,-1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0,-1e9)
    attn = scores.softmax(dim = -1)    
    if dropout is not None:
        attn = dropout(attn)
    return attn @ value     

    


class MultiHeadAttention(nn.Module):
    def __init__(self,h,n_dim,dropout):
        super(MultiHeadAttention,self).__init__()
        assert n_dim % h == 0
        self.d_k = n_dim // h
        self.h = h
        self.query = nn.Linear(n_dim,)
