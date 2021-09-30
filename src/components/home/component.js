import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import moment from 'moment';

import get from 'services/get';
import { truncateText } from 'helpers'

const HomeComponent = (props) => {
  const [lists, setLists] = useState(localStorage.getItem('lists') || '');

  useEffect(async () => {
    async function getLists() {
      const sports = await get('sports.json?errors=0');
      const marketing = await get('marketing.json?errors=0');
      const environment = await get('environment.json?errors=0');
      setLists([...sports.data, ...marketing.data, ...environment.data]);
      localStorage.setItem('lists', [...sports.data, ...marketing.data, ...environment.data]);
    }

    if (!lists) {
      getLists();
    }
  })

  const bookmarkArticle = (list) => {
    console.log('list', list);
  }

  return (
    <div className="container">
      <div className="row">
        {
          lists && lists.map((list, idx) => (
            <div className="col-4" key={idx}>
              <div className="card">
                <img className="card-img-top" src={list.image} alt={list.title} />
                <div className="card-body">
                  <h5 className="card-title">
                    <a href={list.url} target="_blank" rel="noopener noreferrer">{list.title}</a>
                  </h5>
                  <div className="d-flex flex-row justify-content-between">
                    <em className="text-grey">{moment().diff(list.date, "days")} days ago</em>
                    <img src={require('assets/svgs/bookmark.svg').default} className='bookmark-icon' alt='Bookmark' onClick={e => bookmarkArticle(list)} />
                  </div>
                  <p className="card-text">{truncateText(list.content, 50)}</p>
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
