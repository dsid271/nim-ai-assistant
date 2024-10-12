import torch
from transformers import Trainer, TrainingArguments
from src.model_serving.nim_server import NIMServer
from typing import List, Dict

class AdaptiveLearningSystem:
    def __init__(self, nim_server: NIMServer):
        self.nim_server = nim_server

    async def fine_tune(self, dataset: List[Dict[str, str]], epochs: int = 3):
        # Prepare the dataset
        train_dataset = self.prepare_dataset(dataset)

        # Set up training arguments
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
        )

        # Initialize the Trainer
        trainer = Trainer(
            model=self.nim_server.model,
            args=training_args,
            train_dataset=train_dataset,
        )

        # Start fine-tuning
        trainer.train()

        # Update the model in NIMServer
        self.nim_server.model = trainer.model

    def prepare_dataset(self, dataset: List[Dict[str, str]]):
        # Convert the dataset to the format expected by the Trainer
        return [
            {
                "input_ids": self.nim_server.tokenizer.encode(item["input"], return_tensors="pt"),
                "labels": self.nim_server.tokenizer.encode(item["output"], return_tensors="pt"),
            }
            for item in dataset
        ]
