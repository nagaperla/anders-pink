import { SET_DISPLAY_MARKETING, SET_DISPLAY_MARKETING_ERROR } from '../types'

const INITIAL_STATE = {
  marketing: [],
  marketingError: ''
}

const displayImages = (state = INITIAL_STATE, action: any) => {
  const { payload } = action
  switch (action.type) {
    case SET_DISPLAY_MARKETING: {
      return {
        ...state,
        marketing: payload.marketing
      }
    }
    case SET_DISPLAY_MARKETING_ERROR: {
      return {
        ...state,
        marketingError: payload.marketingError
      }
    }
    default:
      return state
  }
}

export default displayImages
