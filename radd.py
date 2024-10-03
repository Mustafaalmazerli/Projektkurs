from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Ladda den större modellen och tokenizern (1.3B)
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

# Samma prompt
prompt = """
Skriv en nyhetsartikel baserad på följande information från en polisrapport:
- Datum: 2024-10-02
- Tid: 14:30
- Plats: Kungsholmen, Stockholm
- Typ av brott: Stöld
"""

inputs = tokenizer(prompt, return_tensors="pt")

# Generera text
outputs = model.generate(
    inputs['input_ids'], 
    attention_mask=inputs['attention_mask'], 
    max_length=300, 
    repetition_penalty=2.0,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

# Dekodera och visa texten
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
