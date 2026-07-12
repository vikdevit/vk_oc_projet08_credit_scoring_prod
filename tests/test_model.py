from src.model_loader import load_model


def test_model_loaded():

    model = load_model()

    assert model is not None
