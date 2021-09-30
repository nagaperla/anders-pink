import axios from 'axios'

export default async function (url, data) {
  return await axios.get(process.env.REACT_APP_ANDERS_PINK_API + url)
}
