import torch

def get_available_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def optimize_model_for_inference(model):
    model.eval()
    if torch.cuda.is_available():
        model = model.half()  # Convert to half precision
    return torch.jit.optimize_for_inference(torch.jit.script(model))

def calculate_model_size(model):
    param_size = 0
    for param in model.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in model.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()
    size_all_mb = (param_size + buffer_size) / 1024**2
    return size_all_mb
