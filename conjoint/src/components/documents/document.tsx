export interface IDocument {
  name: string;
  key: number
}

export const Document = ({ name }: IDocument) => {
  return (
    <li>
      <p>{name}</p>
    </li>
  );
};
