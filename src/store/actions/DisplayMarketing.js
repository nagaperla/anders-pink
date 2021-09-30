import get from 'services/get'

import {
  SET_DISPLAY_MARKETING,
  SET_DISPLAY_MARKETING_ERROR
} from 'store/types'

export const GetDisplayMarketing = (content) => {
  return (dispatch) => {
    get(content.url, content.data).then((res) => {
      dispatch({
        type: SET_DISPLAY_MARKETING,
        payload: {
          marketing: res.data
        }
      })
    }).catch(err => {
      dispatch({
        type: SET_DISPLAY_MARKETING_ERROR,
        payload: {
          marketingError: err
        }
      })
    })
  }
}
