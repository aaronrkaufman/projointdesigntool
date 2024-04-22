import React from 'react';
import { withBemMod } from '@bem-react/core';

import './${block}_${modName}_${modVal}.css';

export interface ${Block}${ModName}${ModVal}Props {
    ${modName}?: '${modVal}';
}

export const with${ModName}${ModVal} = withBemMod<${Block}${ModName}${ModVal}Props>(
    cn${Block}(),
    { ${modName}: '${modVal}' },
    (${Block}) => ({ ...props }) => (
        <${Block} {...props}>
        </${Block}>
    ),
);
