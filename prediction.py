from joblib import load 
import numpy as np
import pickle
import tensorflow as tf

class FirewallModel:

    TF_MODEL_FILE_PATH = './ML_models/model.keras'
    XGB_MODEL_FILE_PATH = './ML_models/xgboost_model.pkl'
    SCALER_PATH = './ML_models/std_scaler.bin'
    LABEL_ENCODER_PATH = './ML_models/label_encoder.bin'
    COLUMNS_ORDER = ['protocol', 'flow_duration', 'tot_fwd_pkts', 'tot_bwd_pkts', 'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std', 'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean', 'bwd_pkt_len_std', 'flow_byts_s', 'flow_pkts_s', 'flow_iat_mean', 'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 'fwd_iat_tot', 'fwd_iat_mean', 'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min', 'bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max', 'bwd_iat_min', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags', 'bwd_urg_flags', 'fwd_header_len', 'bwd_header_len', 'fwd_pkts_s', 'bwd_pkts_s', 'pkt_len_min', 'pkt_len_max', 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var', 'fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt', 'cwe_flag_count', 'ece_flag_cnt', 'down_up_ratio', 'pkt_size_avg', 'fwd_seg_size_avg', 'bwd_seg_size_avg', 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg', 'bwd_blk_rate_avg', 'subflow_fwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_pkts',  'subflow_bwd_byts', 'init_fwd_win_byts', 'init_bwd_win_byts', 'active_mean', 'active_std', 'active_max', 'active_min', 'idle_mean', 'idle_std', 'idle_max', 'idle_min']

    def __init__(self, use_xgboost=True):
        self.use_xgboost = use_xgboost 
        self.model = self.load_model()
        self.scaler = self.load_scaler()
        self.label_encoder = self.load_label_encoder()

    def load_model(self):
        if self.use_xgboost:
            with open(FirewallModel.XGB_MODEL_FILE_PATH, 'rb') as model_file:
                return pickle.load(model_file)
        else:
            return tf.keras.models.load_model(FirewallModel.TF_MODEL_FILE_PATH)

    def load_scaler(self):
        return load(FirewallModel.SCALER_PATH)
    
    def load_label_encoder(self):
        return load(FirewallModel.LABEL_ENCODER_PATH)

    # returns the class and the probability (confidence in prediction)
    def predict(self, data):
        prepared_data = self.prepare_data(data)
        if self.use_xgboost:
            preds = self.model.predict_proba(prepared_data)
        else:
            preds = self.model.predict(prepared_data)
        predicted_classes = np.argmax(preds, axis=1)
        return preds[np.arange(preds.shape[0]), predicted_classes], self.label_encoder.inverse_transform(predicted_classes)

    def prepare_data(self, data): 
        final_data = []
        for flow in data:
            features_list = [flow[feature] for feature in FirewallModel.COLUMNS_ORDER]
            final_data.append(features_list)
        return self.scaler.transform(np.array(final_data))