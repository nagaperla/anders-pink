import { SET_DISPLAY_SPORTS, SET_DISPLAY_SPORTS_ERROR } from '../types'

const INITIAL_STATE = {
  sports: [],
  sportsError: ''
}

const displayImages = (state = INITIAL_STATE, action: any) => {
  const { payload } = action
  switch (action.type) {
    case SET_DISPLAY_SPORTS: {
      return {
        ...state,
        sports: payload.sports
      }
    }
    case SET_DISPLAY_SPORTS_ERROR: {
      return {
        ...state,
        sportsError: payload.sportsError
      }
    }
    default:
      return state
  }
}

export default displayImages
