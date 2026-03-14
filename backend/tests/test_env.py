try:
    import pydantic
    print(f"Pydantic version: {pydantic.__version__}")
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
