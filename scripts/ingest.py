from src.ingestion.loader import load_and_embed_documents

if __name__ == "__main__":
    print("Загружаем и векторизуем документы...")
    load_and_embed_documents()
    print("Готово!")