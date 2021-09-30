import React from 'react'
import { Switch, Route, useLocation } from 'react-router-dom'

import {
  HomeComponent,
  BookmarksComponent,
  DefaultLayoutComponent
} from 'components'

const DefaultRoute = ({path, exact, component}) => (
  <DefaultLayoutComponent>
    <Route key={path} path={path} exact={exact} component={component} />
  </DefaultLayoutComponent>
)

export const Routes = () => {
  const location = useLocation()
  return (
    <Switch location={location} key={location.pathname}>
      <DefaultRoute exact path="/" component={HomeComponent} />
      <DefaultRoute exact path="/bookmarks" component={BookmarksComponent} />
    </Switch>
  )
}

export default Routes
