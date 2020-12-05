from model.CurrentPage import CurrentPage
from model.GettyPictures import GettyPicutes
from model.SearchDetails import SearchDetails
from model.SelectedPictures import SelectedPictures

def factory_models():
    return {"CurrentPage":CurrentPage(),
            "GettyPictures":GettyPicutes(),
            "SearchDetails":SearchDetails(),
            "SelectedPictures":SelectedPictures()}