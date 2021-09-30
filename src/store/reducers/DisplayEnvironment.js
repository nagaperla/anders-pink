import { SET_DISPLAY_ENVIRONMENT, SET_DISPLAY_ENVIRONMENT_ERROR } from '../types'

const INITIAL_STATE = {
  environment: [],
  environmentError: ''
}

const displayImages = (state = INITIAL_STATE, action: any) => {
  const { payload } = action
  switch (action.type) {
    case SET_DISPLAY_ENVIRONMENT: {
      return {
        ...state,
        environment: payload.environment
      }
    }
    case SET_DISPLAY_ENVIRONMENT_ERROR: {
      return {
        ...state,
        environmentError: payload.environmentError
      }
    }
    default:
      return state
  }
}

export default displayImages
