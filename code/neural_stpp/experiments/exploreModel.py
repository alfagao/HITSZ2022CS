from models import CombinedSpatiotemporalModel
from models.spatial import GaussianMixtureSpatialModel
from models.temporal import HawkesPointProcess
import torch

def mi():
    device = torch.device("cpu")
    tpp_model = HawkesPointProcess()
    model = CombinedSpatiotemporalModel(GaussianMixtureSpatialModel(), tpp_model).to(device)
    # # 查看参数
    # print("\t\tname\tparameters")
    # for name, param in model.named_parameters():
    #     print(f"\t\t{name}\t{param}")
    # 加载param <-- ./gmm_hawkes/model.pth
    param_path = "./gmm_hawkes/model.pth"
    state_dict = torch.load(param_path, map_location=torch.device('cpu'))['state_dict']
    model.load_state_dict(state_dict)
    model.eval()
    # how to use this model?
    # def forward(self, event_times, spatial_locations, input_mask, t0, t1)
    t0 = torch.tensor([0.0])
    t1 = torch.tensor([7.0])
    # model.
    model()


if __name__ == '__main__':
    print(torch.tensor([0.0]))






