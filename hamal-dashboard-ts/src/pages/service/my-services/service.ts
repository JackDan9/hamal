import request from 'umi-request';

export async function fakeSubmitMyServices(params: any) {
    return request('/api/my-services', {
        method: 'POST',
        data: params
    });
}
