from model.CurrentPage import CurrentPage
from model.GettyImages import GettyImages
from model.SearchDetails import SearchDetails
from model.SelectedPictures import SelectedPictures

def factory_models():
    return {"CurrentPage":CurrentPage(),
            "GettyPictures":GettyImages(),
            "SearchDetails":SearchDetails(),
            "SelectedPictures":SelectedPictures()}