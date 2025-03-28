import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

access_token = "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"
llama_model = "meta-llama/Llama-2-7b-chat-hf"
#from huggingface_hub import notebook_login
#notebook_login()

class ChatModel():
    def __init__(self, model):
        self.model = model
        if "vicuna" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "lmsys/{}".format(self.model),
                use_fast=False,
            )
            self.generator = AutoModelForCausalLM.from_pretrained(
                "lmsys/{}".format(self.model),
                torch_dtype=torch.float16,
                device_map="auto",
                offload_folder="offload"
            )
        if "llama" in self.model.lower():
            tokenizer = AutoTokenizer.from_pretrained(llama_model, use_auth_token=access_token)
            ll_model = AutoModelForCausalLM.from_pretrained(
                llama_model, 
                use_auth_token=access_token
            )
            pipeline = transformers.pipeline(
                "text-generation",
                model=ll_model,
                torch_dtype=torch.float16,
                device_map="auto",
            )
        elif "gemma" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "google/{}".format(self.model),
                use_fast=False,
            )
            self.generator = AutoModelForCausalLM.from_pretrained(
                "google/{}".format(self.model),
                torch_dtype=torch.float16,
                device_map="auto",
            )

    def chat(self, system_prompt, user_prompt):
        if "llama" in self.model.lower():
            return self.chat_llama2(system_prompt, user_prompt)
        elif "vicuna" in self.model.lower():
            return self.chat_vicuna(system_prompt, user_prompt)
        elif "gemma" in self.model.lower():
            return self.chat_gemma(system_prompt, user_prompt)
        
    def chat_gemma(self, system_prompt, user_prompt):
        prompt = f"<bos><start_of_turn>user\nPlease respond to binary questions.\n\n{system_prompt}\n\n{user_prompt}<end_of_turn>\n<start_of_turn>model"
        
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

    def chat_llama2(self, system_prompt, user_prompt):
            tokenizer = AutoTokenizer.from_pretrained(llama_model, use_auth_token=access_token)
            ll_model = AutoModelForCausalLM.from_pretrained(
                llama_model, 
                use_auth_token=access_token
            )
            pipeline = transformers.pipeline(
                "text-generation",
                model=ll_model,
                torch_dtype=torch.float16,
                device_map="auto",
            )
            sequences = pipeline(
            'Hi! Tell me about yourself!',
            do_sample=True,
            )
            print(sequences[0].get("generated_text"))
       # tokenizer = AutoTokenizer.from_pretrained(model, token=access_token)
       # model = AutoModelForCausalLM.from_pretrained(
        #    model, 
        #    token=access_token
       # )
        
       # dialogs = [
        #    [
          #      {"role": "system", "content": f"Please respond to binary questions.\n\n{system_prompt}"},
          #      {"role": "user", "content": user_prompt},
          #  ],
       # ]
        #response = self.generator.chat_completion(
           # dialogs,  # type: ignore
            #max_gen_len=128,
            #temperature=0.6,
           # top_p=0.9,
        #)

        #return response[0]['generation']['content']
    

    def chat_vicuna(self, system_prompt, user_prompt):
        prompt = f"USER: Please respond to binary questions.\n\n{system_prompt}\n\n{user_prompt}\n\nASSISTANT:"
    
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=512,
                do_sample=True,
                #temperature=0.7,
               # top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
        print(response)
        return str(response)