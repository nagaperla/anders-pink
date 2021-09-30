import get from 'services/get'

import {
  SET_DISPLAY_SPORTS,
  SET_DISPLAY_SPORTS_ERROR
} from 'store/types'

export const GetDisplaySports = (content) => {
  return (dispatch) => {
    get(content.url, content.data).then((res) => {
      dispatch({
        type: SET_DISPLAY_SPORTS,
        payload: {
          sports: res.data
        }
      })
    }).catch(err => {
      dispatch({
        type: SET_DISPLAY_SPORTS_ERROR,
        payload: {
          sportsError: err
        }
      })
    })
  }
}
