import torch
import torch.nn.functional as F

def init_lstm_params(input_sz, hidden_sz):
    #Initialize LSTM Params
    W = torch.randn(4 * hidden_sz, input_sz) * 0.1
    U = torch.randn(4 * hidden_sz, hidden_sz) * 0.1
    b = torch.zeros(4 * hidden_sz)
    return W, U, b
def lstm_cell(x, hidden, W, U, b):
    #LSTM cell forward pass
    h_prev, c_prev = hidden

    #compute all gate inputs
    gates = F.linear(x, W) + F.linear(h_prev, U) + b

    #split gates
    i, f, g, o = gates.chunk(4, 1)

    f = torch.sigmoid(f)
    i = torch.sigmoid(i)
    g = torch.tanh(g)
    o = torch.sigmoid(o)

    #Update cell state 
    c = f * c_prev + i * g
    h = o * torch.tanh(c)
    return h,c

def lstm_forward(x, hidden, params):
    #Forward pass for multi-layer lstm
    W_list, U_list, b_list = params
    h, c = hidden
    output = []
    for t in range(x.size(1)):
        x_t = x[:, t, :]
        for layer in range(len(W_list)):
            h_l, c_l = lstm_cell(x_t,(h[layer], c[layer]), W_list[layer], U_list[layer], b_list[layer])
            h[layer] = h_l
            c[layer] = c_l
            x_t = h_l
        output.append(h[-1])
    output = torch.stack(output, dim=1)
    return output, (h, c)

def create_lstm(input_sz, hidden_sz, num_layers):
    #Create lstm params
    W_list = []
    U_list = []
    b_list = []
    for i in range(num_layers):
        input_layer_size = input_sz if i == 0 else hidden_sz
        W, U, b = init_lstm_params(input_layer_size, hidden_sz)
        W_list.append(W)
        U_list.append(U)
        b_list.append(b)
    return W_list, U_list, b_list

#Example 
input_sz = 10
hidden_sz = 20
num_layers = 2
seq_len = 5
batch_sz = 3

lstm_params = create_lstm(input_sz, hidden_sz, num_layers)

x = torch.randn(batch_sz, seq_len, input_sz)

h = torch.zeros(num_layers, batch_sz, hidden_sz)
c = torch.zeros(num_layers, batch_sz, hidden_sz)

output, (h,c) = lstm_forward(x, (h,c), lstm_params)

print("Output shape:", output.shape)
print("Hidden state shape:", h.shape)
print("Cell state shape:", c.shape)