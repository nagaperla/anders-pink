import React, { Component } from 'react'
import { BrowserRouter as Router } from 'react-router-dom'
import { connect } from 'react-redux'
import Routes from 'routes'

// Importing toastify
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import { GetDisplaySports, GetDisplayMarketing, GetDisplayEnvironment } from 'store/actions'

class AppComponent extends Component {
  constructor(props) {
    super(props);
    this.props = props;
  }

  async componentDidMount() {
    // await this.props.bindDisplaySports({ url: 'sports.json?errors=0' });
    // await this.props.bindDisplayMarketing({ url: 'marketing.json?errors=0' });
    // await this.props.bindDisplayEnvironment({ url: 'environment.json?errors=0' });
  }

  render () {
    return (
      <div>
        <ToastContainer />
        <Router>
          <Routes />
        </Router>
      </div>
    )
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    bindDisplaySports: (content) => dispatch(GetDisplaySports(content)),
    bindDisplayMarketing: (content) => dispatch(GetDisplayMarketing(content)),
    bindDisplayEnvironment: (content) => dispatch(GetDisplayEnvironment(content))
  }
}

export default connect(
  null,
  mapDispatchToProps
)(AppComponent)
