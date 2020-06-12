import { Effect, Reducer } from 'umi';

import { fakeSubmitMyServices } from './service';

export interface MyServicesStateType {

}

export interface ModelType {
    namespace: string;
}

const Model: ModelType = {
    namespace: 'serviceAndmyServices',

    state: {
        
    },

    effects: {

    },

    reducers: {
        saveCurrentStep(state, { payload }) {
            return {
                ...state,
                current: payload,
            };
        },
    }
};

export default Model;
