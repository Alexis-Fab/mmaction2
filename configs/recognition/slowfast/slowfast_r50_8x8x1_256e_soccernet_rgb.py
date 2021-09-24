_base_ = ['./slowfast_r50_4x16x1_256e_soccernet_rgb.py']

model = dict(
    backbone=dict(
        resample_rate=4,  # tau
        speed_ratio=4,  # alpha
        channel_ratio=8,  # beta_inv
        slow_pathway=dict(fusion_kernel=7)))

# work_dir = './work_dirs/test20210920-1'
work_dir = './work_dirs/sf50_8x8x1_2021_09_20_NoAction'
# resume_from = './work_dirs/sf50_8x8x1_2021_09_13_NoAction/latest.pth'
