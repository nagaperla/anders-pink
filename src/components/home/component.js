import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';

import get from 'services/get';

const HomeComponent = (props) => {
  const [lists, setLists] = useState('');

  useEffect(async () => {
    async function getLists() {
      const sports = await get('sports.json?errors=0');
      const marketing = await get('marketing.json?errors=0');
      const environment = await get('environment.json?errors=0');
      setLists([...sports.data, ...marketing.data, ...environment.data]);
    }

    if (!lists) {
      getLists();
    }
  })

  return (
    <div className="container">
      <div className="row">
        {
          lists && lists.map((list, idx) => (
            <div className="col-4">
              <div className="card" key={idx}>
                <img className="card-img-top" src={list.image} alt={list.title} />
                <div className="card-body">
                  <h5 className="card-title">
                    <span>{list.title}</span>
                    <span>Bookmark</span>
                  </h5>
                  <a href={list.url} className="btn btn-primary" target="_blank" rel="noopener noreferrer">Go somewhere</a>
                  <p className="card-text">{list.content}</p>
                </div>
              </div>
            </div>
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
