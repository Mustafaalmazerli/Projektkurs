# import pandas as pd

# Läs in CSV-filen
# df = pd.read_csv('s.csv')

# Använd en funktion för att ta bort datum och plats
#def rensa_rad(rad):
   # delar = rad.split(", ")  # Dela upp baserat på komma och mellanslag
    #if len(delar) >= 3:
        # Behåll endast "Ofredande/förargelse" (andra delen av raden)
      #  return delar[1]
   # return rad  # Om något går fel behåll originalrad

# Tillämpa funktionen på 'Rubrik'-kolumnen (eller den kolumn där dina rader finns)
#df['Rubrik'] = df['Rubrik'].apply(rensa_rad)

# Spara den bearbetade filen
#df.to_csv('bearbetad_fil.csv', index=False)
from transformers import AutoTokenizer, AutoModelForCausalLM

# Ladda GPT-J 6B
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

# Samma prompt
prompt = """
Skriv en nyhetsartikel baserad på följande information från en polisrapport:
- Datum: 2024-10-02
- Tid: 14:30
- Plats: Kungsholmen, Stockholm
- Typ av brott: Stöld
- Händelseförlopp: En person stal en cykel från en cykelparkering nära Stadshuset. En förbipasserande försökte stoppa tjuven men misslyckades. Polisen söker nu vittnen.
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

