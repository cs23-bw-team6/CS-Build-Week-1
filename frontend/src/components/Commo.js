import React from 'react';
import { axiosWithAuth } from '../axiosWithAuth';
import regeneratorRuntime from "regenerator-runtime";

import '../scss/Commo.scss';

const Commo = ({ fetchPlayerData, player, holding, pickup }) => {
  async function getItem(item) {
    try {
      const { data } = await axiosWithAuth().post('adv/get_item', {
        item: item
      });
      console.log('getItem() data', data);
      pickup([...holding, item]);
      fetchPlayerData();
    } catch (err) {
      console.error(err);
    }
  }

  async function playItem(item) {
    try {
      const { data } = await axiosWithAuth().post('adv/use_item/', {
        item: item
      });
      console.log('useItem() data', data);
      if (
        data.msg === 'Keep searching for the treasure!' ||
        data.msg === 'The chest for this key is not in here!'
      ) {
        const drop = holding.filter(i => i !== item);
        pickup(drop);
      } else {
        console.log('WOWOWOW YOU WIN!');
        spawn();
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function spawn() {
    try {
      const { data } = await axiosWithAuth().get('adv/spawn/');
      console.log('Commo.js spawn() data', data);
      window.location.reload();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <section className="Commo">
      {player ? (
        <>
          <div className="room-description">
            <header>{player.title}</header>
            <p>{player.description}</p>
          </div>
          <div className="holding-items">
            You have:{' '}
            {holding.map(item => {
              return (
                <div className="held-item" onClick={() => playItem(item)}>
                  {item}
                </div>
              );
            })}
          </div>
          <div className="room-items">
            Items here:{' '}
            {player.items.map(item => {
              return (
                <div className="get-item" onClick={() => getItem(item)}>
                  {item}
                </div>
              );
            })}
          </div>

          <div className="room-containers">
            Containers here:{' '}
            {player.containers.map(chest => {
              return <div className="chest">{chest}</div>;
            })}
          </div>
        </>
      ) : (
        <div className="loading">Loading...</div>
      )}
    </section>
  );
};

export default Commo;
