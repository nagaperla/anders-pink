import React from 'react'
import { Switch, Route } from 'react-router-dom'

import { DefaultLayoutComponent } from 'components'

const DefaultRoute = ({path, exact, component}) => (
  <DefaultLayoutComponent>
    <Route key={path} path={path} exact={exact} component={component} />
  </DefaultLayoutComponent>
)

export const Routes = () => {
  return (
    <Switch>
      <DefaultRoute exact path="/" component={DefaultLayoutComponent} />
      <DefaultRoute exact path="/bookmarks" component={DefaultLayoutComponent} />
    </Switch>
  )
}

export default Routes
