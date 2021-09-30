import React from "react";
import moment from 'moment';
import { truncateText } from 'helpers';

const CardComponent = (article) => {
  const bookmarkArticle = () => {
    console.log(article);
  }

  return (
    <div className="col-4">
      <div className="card">
        <img className="card-img-top" src={article.image} alt={article.title} />
        <div className="card-body">
          <h5 className="card-title">
            <a href={article.url} target="_blank" rel="noopener noreferrer">{article.title}</a>
          </h5>
          <div className="d-flex flex-row justify-content-between">
            <em className="text-grey">{moment().diff(article.date, "days")} days ago</em>
            <img src={require('assets/svgs/bookmark.svg').default} className='bookmark-icon' alt='Bookmark' onClick={bookmarkArticle} />
          </div>
          <p className="card-text">{truncateText(article.content, 50)}</p>
        </div>
      </div>
    </div>
  )
}

export default CardComponent;
