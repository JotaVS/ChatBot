import spacy
from spacy.matcher import Matcher
import wikipedia
import random

nlp = spacy.load('pt_core_news_sm')

padrao_saudacao = [
    [{"LOWER": {"IN": ["oi", "olá", "oi!", "olá!", "ola", "ola!"]}}]
]

padrao_informacao = [
    [{"LOWER": {"IN": ["o que", "como", "quem", "quando", "onde", "por que", "qual", "sobre", "fale", "fala"]}}],

]

padrao_despedida = [
    [{"LOWER": {"IN": ["tchau", "adeus", "falou", "sair"]}}],
]

respostas_saudacao = [
    "Olá! Como posso ajudar?",
    "Oi! Em que posso ser útil?",
    "Olá, tudo bem? Como posso ser útil hoje?"
]

respostas_informacao = [
    "Aqui estão algumas informações para você:",
    "Eu posso fornecer informações sobre isso:",
    "Vamos ver o que posso encontrar para você:",
]

respostas_despedida = [
    "Até logo! Se precisar, estarei aqui.",
    "Tchau! Espero ter ajudado.",
    "Falou! Volte sempre que precisar.",
]


def buscar_sobre(assunto):
    try:
        wikipedia.set_lang("pt")
        descricao = wikipedia.summary(assunto, sentences=2)
        return descricao
    except wikipedia.exceptions.WikipediaException:
        return f"Não foi encontrada nenhuma informação sobre " + assunto + "."


def detectar_intencao(text):
    doc = nlp(text.lower())

    matcher = Matcher(nlp.vocab)
    matcher.add("Saudacao", padrao_saudacao)
    matcher.add("Informacao", padrao_informacao)
    matcher.add("Despedida", padrao_despedida)

    matches = matcher(doc)

    if matches:
        for match_id, start, end in matches:
            if nlp.vocab.strings[match_id] == "Saudacao":
                return random.choice(respostas_saudacao)
            elif nlp.vocab.strings[match_id] == "Informacao":
                if not doc.ents:
                    return "Não consegui identificar sobre o que você quer saber, por favor reformule a pergunta!"
                else:
                    print("Bot: " + random.choice(respostas_informacao))
                    return buscar_sobre(doc.ents[0].text)
            elif nlp.vocab.strings[match_id] == "Despedida":
                print("Bot: " + random.choice(respostas_despedida))
                return "sair"
    else:
        return "Desculpe, não entendi. Poderia repetir?"


def chatbot_main():
    print("Olá! Eu sou um chatbot simples. Você pode começar me cumprimentando!")
    print("Você pode sair a qualquer momento digitando 'sair'.\n")

    while True:
        entrada_usuario = input("Você: ").strip().lower()

        resposta = detectar_intencao(entrada_usuario)

        if resposta == "sair":
            break
        if resposta:
            print("Bot: " + resposta)
        else:
            print("Bot: Desculpe, não entendi. Você pode repetir?")


if __name__ == "__main__":
    chatbot_main()
