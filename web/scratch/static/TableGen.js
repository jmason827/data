export class TableGen {
    constructor( data=[] ) {
      this.data = data;
      this.rowListener = null;
      this.colListener = null;
      this.headerListener = null;
      this.cellListener = null;
      this.table = null;
    }
  
    setRowListener(fn)    { this.rowListener    = fn; this._attachListener(); }
    setColumnListener(fn) { this.colListener    = fn; this._attachListener(); }
    setHeaderListener(fn) { this.headerListener = fn; this._attachListener(); }
    setCellListener(fn)   { this.cellListener   = fn; this._attachListener(); }
  
    _attachListener() {
      if(this.table && !this._listenerAttached) {
        this.table.addEventListener('click', (e) => this._handleClick(e));
        this._listenerAttached = true;
      }
    }
  
    _handleClick(e) {
      if(e.target.matches('th') && this.headerListener) {
        this.headerListener(e);
        return;
      }
      if(!e.target.matches('td')) return;
      if(this.cellListener) this.cellListener(e);
      const row = e.target.closest('tr'), body = row?.parentNode;
      if(body && this.rowListener) this.rowListener(e);
      if(body && this.colListener) {
        const colIndex = [...row.cells].indexOf(e.target);
        this.colListener(colIndex, e);
      }
    }
  
    rowsToTable(data=this.data) {
      const cols = [...new Set(data.flatMap(Object.keys))];
      this.table = document.createElement('table');
      const thead = this.table.createTHead(), tbody = this.table.createTBody();
      thead.insertRow().append(...cols.map(c => Object.assign(document.createElement('th'), {textContent: c})));
      data.forEach(rowObj => {
        const tr = tbody.insertRow();
        cols.forEach(c => tr.insertCell().textContent = rowObj[c] ?? '');
      });
      this._attachListener();
      return this.table;
    }
  
    toRows() {
      if (!this.table || !this.table.tHead || !this.table.tBodies[0]) return [];
      const cols = [...this.table.tHead.rows[0].cells].map(th => th.textContent);
      return [...this.table.tBodies[0].rows].map(tr =>
        Object.fromEntries([...tr.cells].map((td, i) => [cols[i], td.textContent]))
      );
    }
  }
  