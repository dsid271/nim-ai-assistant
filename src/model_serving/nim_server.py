import yaml
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class NIMServer:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() and self.config['optimization']['use_cuda'] else "cpu")
        self.tokenizer = None
        self.model = None

    @staticmethod
    def load_config(config_path: str):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    async def initialize(self):
        model_config = self.config['model']
        optimization_config = self.config['optimization']

        print(f"Initializing NIM server with model: {model_config['name']}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_config['name'],
            revision=model_config['revision'],
            **model_config['tokenizer']
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_config['name'],
            revision=model_config['revision'],
            torch_dtype=torch.float16 if optimization_config['use_fp16'] else torch.float32,
            device_map=optimization_config['device_map']
        )

        if self.device.type == 'cuda':
            self.model = self.model.to(self.device)

        print("NIM server initialized successfully")

    async def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        generation_config = self.config['model']['generation']
        
        outputs = self.model.generate(
            **inputs,
            **generation_config
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    @classmethod
    async def create(cls, config_path: str):
        server = cls(config_path)
        await server.initialize()
        return server
