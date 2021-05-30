import request from './request'

export const posttest = postFrom => request({
  url: '',
  method: 'post',
  data: postFrom
})

export const getTest = queryData => request({
  url: 'http://47.241.170.143:3410/devices/regions',
  method: 'get',
  data: queryData
})
