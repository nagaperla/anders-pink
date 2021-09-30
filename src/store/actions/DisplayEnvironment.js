import get from 'services/get'

import {
  SET_DISPLAY_ENVIRONMENT,
  SET_DISPLAY_ENVIRONMENT_ERROR
} from 'store/types'

export const GetDisplayEnvironment = (content) => {
  return (dispatch) => {
    get(content.url, content.data).then((res) => {
      dispatch({
        type: SET_DISPLAY_ENVIRONMENT,
        payload: {
          environment: res.data
        }
      })
    }).catch(err => {
      dispatch({
        type: SET_DISPLAY_ENVIRONMENT_ERROR,
        payload: {
          environmentError: err
        }
      })
    })
  }
}
