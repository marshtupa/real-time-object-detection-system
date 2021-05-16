from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog
import numpy as np
from PIL import Image


class Detectron2Client:

    def __init__(self):
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = "cpu"
        self.model = 'mask_rcnn_R_50_FPN_3x.yaml'
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/" + self.model))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/" + self.model)

    def predict(self, image):
        predictor = DefaultPredictor(self.cfg)
        return predictor(image)

    def draw_result_to_image(self, image, output):
        metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
        v = Visualizer(image[:, :, ::-1], metadata=metadata, scale=1.2)
        v = v.draw_instance_predictions(output["instances"].to("cpu"))
        image = Image.fromarray(np.uint8(v.get_image()[:, :, ::-1]))
        return image

    def inference(self, image):
        output = self.predict(image)
        image = self.draw_result_to_image(image, output)
        return image
