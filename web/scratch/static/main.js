import { TableGen } from './TableGen.js'; // Adjust path if needed

function generatePlaceholderData(namePrefix) {
  // Make each data set slightly different
  return [
    { timestamp: '2024-12-12 10:00:00', part_number: namePrefix+'123', message: 'Hello' },
    { timestamp: '2024-12-12 10:05:00', part_number: namePrefix+'456', message: 'World' },
    { timestamp: '2024-12-12 10:10:00', part_number: namePrefix+'999', message: 'Testing' }
  ];
}

document.addEventListener('DOMContentLoaded', () => {
  const table1 = new TableGen(generatePlaceholderData('ABC'));
  const table2 = new TableGen(generatePlaceholderData('XYZ'));
  const table3 = new TableGen(generatePlaceholderData('FOO'));
  const table4 = new TableGen(generatePlaceholderData('BAR'));

  // Build each table
  const tableElm1 = table1.rowsToTable();
  const tableElm2 = table2.rowsToTable();
  const tableElm3 = table3.rowsToTable();
  const tableElm4 = table4.rowsToTable();

  // Insert tables into their respective grid cells
  document.getElementById('slot1').appendChild(tableElm1);
  document.getElementById('slot2').appendChild(tableElm2);
  document.getElementById('slot3').appendChild(tableElm3);
  document.getElementById('slot4').appendChild(tableElm4);
});
