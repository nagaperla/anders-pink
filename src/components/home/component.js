import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';

import { CardComponent } from 'components';
import get from 'services/get';

const HomeComponent = (props) => {
  const [lists, setLists] = useState(JSON.parse(localStorage.getItem('lists')) || '');

  useEffect(async () => {
    async function getLists() {
      const sports = await get('sports.json?errors=0');
      const marketing = await get('marketing.json?errors=0');
      const environment = await get('environment.json?errors=0');
      setLists([...sports.data, ...marketing.data, ...environment.data]);
      localStorage.removeItem('lists');
      localStorage.setItem('lists', JSON.stringify([...sports.data, ...marketing.data, ...environment.data]));
    }

    if (!lists) {
      getLists();
    }
  })

  return (
    <div className="container">
      <div className="row">
        {
          lists && lists.map((article, idx) => (
            <CardComponent article={article} key={idx} />
          ))
        }
      </div>
    </div>
  )
}

const mapStateToProps = (state) => {
  const { sports, sportsError } = state.displaySports
  const { marketing, marketingError } = state.displayMarketing
  const { environment, environmentError } = state.displayEnvironment
  return { sports, sportsError, marketing, marketingError, environment, environmentError }
}

export default connect(
  mapStateToProps,
  null
)(HomeComponent)
