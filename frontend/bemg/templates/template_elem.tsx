import React, { FC } from 'react';

import styles from './${block}__${elem}.module.css';

export interface ${Block}${Elem}Props {
}

export const ${Block}${Elem}: FC<${Block}${Elem}Props> = ({  }) => (
    <div className={styles.${block}__${elem}}>{}</div>
);

