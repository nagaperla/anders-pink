import { combineReducers } from 'redux'
import displaySports from './DisplaySports'
import displayMarketing from './DisplayMarketing'
import displayEnvironment from './DisplayEnvironment'

export default combineReducers({
  displaySports,
  displayMarketing,
  displayEnvironment
})
