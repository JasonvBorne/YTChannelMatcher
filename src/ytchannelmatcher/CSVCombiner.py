import os
import pandas as pd
import  numpy as np
from glob import glob

class CSVCombiner:
    def __init__(self, input_dir='../../result/data/order_relevance', output_file='../../result/combined_channels.csv', decay_factor=0.5):
        self.input_dir = input_dir
        self.output_file = output_file
        self.decay_factor = decay_factor

    def _apply_weight(self, df: pd.DataFrame, file_idx: int) -> pd.DataFrame:
        """
        仅按行序号计算权重：
            weight = decay_factor ** row_position
        行越靠前，权重越高；文件顺序不再参与计算。
        """
        df = df.copy().reset_index(drop=True)
        row_positions = np.arange(len(df))
        df['weight'] = self.decay_factor ** row_positions
        return df

    def combine_csv_files(self):
        # 获取所有 CSV 文件路径
        all_files = glob(os.path.join(self.input_dir, '*.csv'))

        # 读取 CSV 并添加权重列（按文件顺序指数衰减）
        df_list = []
        for idx, file in enumerate(all_files):
            df = pd.read_csv(file)
            df = self._apply_weight(df, idx)
            df_list.append(df)

        # 只保留需要的列
        combined_df = pd.concat(df_list, ignore_index=True)

        combined_df = combined_df[['videoId', 'channelId', 'channelTitle', 'weight']]

        # 按 channelId 聚合
        result_df = combined_df.groupby(['channelId', 'channelTitle']).agg({
            'videoId': lambda ids: ','.join(ids),
            'weight': 'max'        # 取同频道最大权重
        }).reset_index()

        # 添加 videoCount 列
        result_df['videoCount'] = result_df['videoId'].apply(lambda x: len(x.split(',')))

        # 按权重总和降序排序
        result_df = result_df.sort_values(by='weight', ascending=False)

        # 保存结果
        result_df.to_csv(self.output_file, index=False)
        print(f"✅ 合并完成，保存为：{self.output_file}")

# 使用示例
if __name__ == '__main__':
    combiner = CSVCombiner(decay_factor=0.99)
    # combiner = CSVCombiner()
    combiner.combine_csv_files()