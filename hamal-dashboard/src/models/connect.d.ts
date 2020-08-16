import { MenuDataItem } from '@ant-design/pro-layout';
// import { GlobalModelState } from './global';
import { DefaultSettings as SettingModelState } from '../../config/defaultSettings';
// import { UserModelState } from './user';
// import { StateType } from './login';

export { SettingModelState };

export interface Loading {

}

export interface ConnectState {
    settings: SettingModelState;
}

export interface Route extends MenuDataItem {
    routes?: Route[];
}
