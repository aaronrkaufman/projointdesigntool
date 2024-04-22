import React, { FC } from 'react';

import styles from './${block}.module.css';

export interface ${Block}Props{
}

export const ${Block}: FC<${Block}Props> = ({ }) => {
  return <div className={styles.${block}}></div>;
};
