from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model = AutoModelForSeq2SeqLM.from_pretrained("./model/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("./model/opus-mt-en-zh")
translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)
# text = "Physics is the natural science that studies matter, its fundamental constituents, its motion and behavior through space and time, and the related entities of energy and force"
text = "Physics is one of the oldest academic disciplines and, through its inclusion of astronomy, perhaps the oldest."
result = translation(text)
print(result)