import React from 'react';
import ReactDOM from 'react-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Popover from 'react-bootstrap/Popover'
import Jumbotron from 'react-bootstrap/Jumbotron';
import InputGroup from 'react-bootstrap/InputGroup';
import ReactHtmlParser from 'react-html-parser';
import axios from 'axios';
import Parser from 'html-react-parser'
import {Bars} from 'svg-loaders-react'


class ChemicalSearchPageApp extends React.Component {
  constructor(props) {
    const defaultSearchType = 'name';
    const defaultFilterProp = 'mp';
    super(props)
    this.state = {
      searchType: defaultSearchType,
      searchTerm: '',
      resultsSectionDisplay: 'none',
      resultsSectionHTML: '',
      searchInputsFormValidated: false,
      numActivePropFilters: 0,
      requireSearchTerm: false,
      searchTermReqPopDisplay: 'none',
      searchTermInputDisabled: false,
      searchSpinnerDisplay: 'none',
      propFilters: {
        1: {
          'display': 'none',
          'prop': defaultFilterProp,
          'min': null,
          'max': null,
          'allowPreds': true,
          'removeFilterBtnDisplay': 'block',
        },
        2: {
          'display': 'none',
          'prop': defaultFilterProp,
          'min': null,
          'max': null,
          'allowPreds': true,
          'removeFilterBtnDisplay': 'block',
        },
        3: {
          'display': 'none',
          'prop': defaultFilterProp,
          'min': null,
          'max': null,
          'allowPreds': true,
          'removeFilterBtnDisplay': 'block',
        },
        4: {
          'display': 'none',
          'prop': defaultFilterProp,
          'min': null,
          'max': null,
          'allowPreds': true,
          'removeFilterBtnDisplay': 'block',
        },
        5: {
          'display': 'none',
          'prop': defaultFilterProp,
          'min': null,
          'max': null,
          'allowPreds': true,
          'removeFilterBtnDisplay': 'block',
        }
      }
    };
    this.handleSearchTypeSelectChange =
      this.handleSearchTypeSelectChange.bind(this)
    this.handleAddFilterBtnClick = this.handleAddFilterBtnClick.bind(this)
    this.handleSearchBtnClick = this.handleSearchBtnClick.bind(this)
    this.handleSearchTermChange = this.handleSearchTermChange.bind(this)
    this.handleFilterMinValChange = this.handleFilterMinValChange.bind(this)
    this.handleFilterMaxValChange = this.handleFilterMaxValChange.bind(this)
    this.handleFilterPropSelectChange =
      this.handleFilterPropSelectChange.bind(this)
    this.handleRemoveFilterBtnClick =
      this.handleRemoveFilterBtnClick.bind(this)
    this.handleAllowPredValsCheckboxChange =
      this.handleAllowPredValsCheckboxChange.bind(this)
    this.handleEnterKeyUp =
      this.handleEnterKeyUp.bind(this)
  }

  handleEnterKeyUp(event) {
    var code = event.keyCode || event.which;
    if (code === 13) {
      this.handleSearchBtnClick(event)//13 is the enter keycode
      //Do stuff in here
    }
  }

  handleFilterMinValChange(event) {
    var val = event.target.value
    var id = event.target.id
    var propFilters = this.state.propFilters
    propFilters[id]['min'] = val;
    this.setState({
      propFilters: propFilters
    })
  }

  handleFilterMaxValChange(event) {
    var val = event.target.value
    var id = event.target.id
    var propFilters = this.state.propFilters
    propFilters[id]['max'] = val;
    this.setState({
      propFilters: propFilters
    })
  }

  handleFilterPropSelectChange(event) {
    var prop = event.target.value
    var id = event.target.id
    var propFilters = this.state.propFilters
    propFilters[id]['prop'] = prop;
    this.setState({
      propFilters: propFilters
    })
  }

  handleSearchTermChange(event) {
    var searchTerm = event.target.value
    this.setState({
      searchTerm: searchTerm,
      searchTermReqPopDisplay: 'none'
    })
  }

  handleSearchTypeSelectChange(event) {
    var searchType = event.target.value
    var propFilters = this.state.propFilters
    if (searchType === 'all') {
      if (this.state.numActivePropFilters === 0) {
        this.handleAddFilterBtnClick(event)
      }
      propFilters[1]['removeFilterBtnDisplay'] = 'none'
      this.setState({
        searchTermInputDisabled: true,
        searchTerm: '',
        propFilters: propFilters
      })
    } else {
      propFilters[1]['removeFilterBtnDisplay'] = 'block'
      this.setState({
        searchTermInputDisabled: false,
        propFilters: propFilters
      })
    }
    this.setState({
      searchType: searchType,
      resultsSectionDisplay: 'none',
    })
  }

  handleAddFilterBtnClick(event) {
    var propFilters = this.state.propFilters;
    var numActivePropFilters = this.state.numActivePropFilters;
    propFilters[numActivePropFilters + 1]['display'] = 'block';
    this.setState({
      propFilters: propFilters,
      numActivePropFilters: numActivePropFilters + 1
    })
  }

  handleRemoveFilterBtnClick(event) {
    var propFilters = this.state.propFilters;
    var numActivePropFilters = this.state.numActivePropFilters;
    propFilters[event.target.id] = {
      'display': 'none',
      'prop': null,
      'min': null,
      'max': null,
    }
    this.setState({
      propFilters: propFilters,
      numActivePropFilters: numActivePropFilters - 1
    })
  }

  handleAllowPredValsCheckboxChange(event) {
    var propFilters = this.state.propFilters;
    if (propFilters[event.target.id]['allowPreds']) {
      propFilters[event.target.id]['allowPreds'] = false
    } else {
      propFilters[event.target.id]['allowPreds'] = true
    }
    this.setState({
      propFilters: propFilters,
    })
  }

  handleSearchBtnClick(event) {

    // first validate search term (i.e. ensure it is not blank)
    if (this.state.requireSearchTerm) {
      if (this.state.searchTerm === '') {
        this.setState({
          searchTermReqPopDisplay: 'block',
        })
        return
      }
    }
    this.setState({
      searchSpinnerDisplay: 'block',
      resultsSectionDisplay: 'none',
    })

    // Initialize query string params.
    var params = {
      searchType: this.state.searchType,
      searchTerm: this.state.searchTerm,
    }
    const propFilters = this.state.propFilters;
    for (var i in propFilters) {
      var filter = propFilters[i]
      // Only get min/max criteria from filters that are visible (i.e. the
      // user has 'turned on').
      if (filter['display'] === 'block') {
        // Generate query string key for min/max prop vals
        // to be included in AJAX call.
        const propMinQsKey = `${filter['prop']}Min`
        const propMaxQsKey = `${filter['prop']}Max`
        const propAllowPredsKey = `${filter['prop']}AllowPreds`
        if (filter['min'] !== null) {
          params[propMinQsKey] = `${filter['min']}`
        }
        if (filter['max'] !== null) {
          params[propMaxQsKey] = `${filter['max']}`
        }
        params[propAllowPredsKey] = `${filter['allowPreds']}`
      }
    }
    axios.get(
      'results', {
        params: params
      }
    ).then(
      res => {
        console.log(res.data)
        // If search type is SMILES and a result is found, bypass rendering
        // a search results section and go straight to the chemical's detail
        // page.
        if (this.state.searchType === 'smiles' && 'chem_pk' in res.data) {
          var getUrl = window.location;
          var baseUrl = getUrl.protocol
            + "//" + getUrl.host
            + "/" + getUrl.pathname.split('/')[1];
          window.location.href = `${baseUrl}/detail/${res.data.chem_pk}/`;

        // For all non-SMILES search types, render the results table
        } else {
          // Remove the extra whitespace between HTML tags in the returned
          // string. This is needed to supress warnings from the React
          // virtual DOM.
          const html = res.data.html.replace(/>\s+</g, "><");
          this.setState({
            resultsSectionDisplay: 'block',
            resultsSectionHTML: html,
            searchSpinnerDisplay: 'none'
          })
        }
      }
    )
  }

  render() {
    return (
      <Container>
        <br></br>
        <h2>Molecule Explorer</h2>
        <SearchInputsJumbo
          searchType={this.state.searchType}
          searchTypeSelectOnChange={this.handleSearchTypeSelectChange}
          propFilters={this.state.propFilters}
          addFilterBtnOnClick={this.handleAddFilterBtnClick}
          removeFilterBtnOnClick={this.handleRemoveFilterBtnClick}
          allowPredValsCheckboxOnChange={this.handleAllowPredValsCheckboxChange}
          filterPropSelectOnChange={this.handleFilterPropSelectChange}
          searchBtnOnClick={this.handleSearchBtnClick}
          searchTermOnChange={this.handleSearchTermChange}
          filterMaxValOnChange={this.handleFilterMaxValChange}
          filterMinValOnChange={this.handleFilterMinValChange}
          searchTermReqPopDisplay={this.state.searchTermReqPopDisplay}
          enterOnKeyUp={this.handleEnterKeyUp}
          searchTermVal={this.state.searchTerm}
          searchTermInputDisabled={this.state.searchTermInputDisabled}
        />
        <Form onSubmit={this.handleSearchBtnClick}
              className={
                this.state.inputParamsFormValidated ? "was-validated" : ""
              }
              noValidate
        />
        <SearchResults
          html={this.state.resultsSectionHTML}
          display={this.state.resultsSectionDisplay}
          searchSpinnerDisplay={this.state.searchSpinnerDisplay}
        />
      </Container>
    );
  }
}

class SearchResults extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div
      >
        <div className="d-flex justify-content-md-center">
          <Bars stroke="#aba9a9"
                style={{
                  'display': this.props.searchSpinnerDisplay,
                  'width': 100
                }}
          />
        </div>
        <div
          style={{display: this.props.display}}>
          {Parser(this.props.html)}
        </div>
      </div>
    )
  }
}


class SearchInputsJumbo extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <Jumbotron style={{padding: "2% 3%"}}>
        {/*<Form onSubmit={this.props.nextBtnOnClick}>*/}
        <Form
          autoComplete={'off'}
        >
          <Form.Group>
            <Row>
              <p className={'mx-3'}>
                Search for desired molecules using the different identifiers
                below.
                Use "Add Filter" to search for multiple molecules within
                property ranges. If available, experimental values are listed.
                Click on a desired molecule to see predicted property values if
                experimental values are not available.
              </p>
            </Row>
            <Row>
              <Col xs={3}>
                <Form.Label className="mr-1">
                  <strong>Search By</strong>
                </Form.Label>
                <Form.Control
                  required
                  as="select"
                  size="md"
                  style={{width: 210}}
                  defaultValue={this.props.searchType}
                  onChange={this.props.searchTypeSelectOnChange}
                >
                  <option value='name'>Molecular Name</option>
                  <option value='smiles'>SMILES</option>
                  <option value='iupac'>IUPAC</option>
                  <option value='inchi'>InChIKey</option>
                  <option value='formula'>Molecular Formula</option>
                  <option value='all'>Search All Molecules</option>
                </Form.Control>
              </Col>
              <Col lg>
                <Form.Label className="mr-1">
                  <strong>Search Term</strong>
                </Form.Label>
                <Form.Control
                  style={{width: 250}}
                  onChange={this.props.searchTermOnChange}
                  value={this.props.searchTermVal}
                  onKeyUp={this.props.enterOnKeyUp}
                  disabled={this.props.searchTermInputDisabled}
                />
                <Popover id="popover-basic"
                         placement={'right'}
                         show={false}
                         style={{
                           'marginLeft': 280,
                           'marginTop': 30,
                           'display': this.props.searchTermReqPopDisplay
                           // 'display': 'none'
                         }}
                >
                  <Popover.Content>
                    <strong>Search Term Required</strong>
                  </Popover.Content>
                </Popover>
              </Col>
            </Row>
          </Form.Group>
          <Form.Group>
            <div style={{display: this.props.propFilters[1]['display']}}>
              <PropFilter
                id={1}
                removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}
                removeFilterBtnDisplay={
                  this.props.propFilters[1]['removeFilterBtnDisplay']
                }
                filterPropSelectOnChange={this.props.filterPropSelectOnChange}
                filterMinValOnChange={this.props.filterMinValOnChange}
                filterMaxValOnChange={this.props.filterMaxValOnChange}
                allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}
                enterOnKeyUp={this.props.enterOnKeyUp}
              />
            </div>
            <div style={{display: this.props.propFilters[2]['display']}}>
              <PropFilter
                id={2}
                removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}
                removeFilterBtnDisplay={
                  this.props.propFilters[2]['removeFilterBtnDisplay']
                }
                filterPropSelectOnChange={this.props.filterPropSelectOnChange}
                filterMinValOnChange={this.props.filterMinValOnChange}
                filterMaxValOnChange={this.props.filterMaxValOnChange}
                allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}
                enterOnKeyUp={this.props.enterOnKeyUp}
              />
            </div>
            <div style={{display: this.props.propFilters[3]['display']}}>
              <PropFilter
                id={3}
                removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}
                removeFilterBtnDisplay={
                  this.props.propFilters[3]['removeFilterBtnDisplay']
                }
                filterPropSelectOnChange={this.props.filterPropSelectOnChange}
                filterMinValOnChange={this.props.filterMinValOnChange}
                filterMaxValOnChange={this.props.filterMaxValOnChange}
                allowPredValsCheckboxOnChange={
                  this.props.allowPredValsCheckboxOnChange
                }
                enterOnKeyUp={this.props.enterOnKeyUp}
              />
            </div>
            <div style={{display: this.props.propFilters[4]['display']}}>
              <PropFilter
                id={4}
                removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}
                removeFilterBtnDisplay={
                  this.props.propFilters[4]['removeFilterBtnDisplay']
                }
                filterPropSelectOnChange={this.props.filterPropSelectOnChange}
                filterMinValOnChange={this.props.filterMinValOnChange}
                filterMaxValOnChange={this.props.filterMaxValOnChange}
                allowPredValsCheckboxOnChange={
                  this.props.allowPredValsCheckboxOnChange
                }
                enterOnKeyUp={this.props.enterOnKeyUp}
              />
            </div>
            <div style={{display: this.props.propFilters[5]['display']}}>
              <PropFilter
                id={5}
                removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}
                filterPropSelectOnChange={this.props.filterPropSelectOnChange}
                removeFilterBtnDisplay={
                  this.props.propFilters[5]['removeFilterBtnDisplay']
                }
                filterMinValOnChange={this.props.filterMinValOnChange}
                filterMaxValOnChange={this.props.filterMaxValOnChange}
                allowPredValsCheckboxOnChange={
                  this.props.allowPredValsCheckboxOnChange
                }
                searchBtnOnClick={this.props.searchBtnOnClick}
                enterOnKeyUp={this.props.enterOnKeyUp}
              />
            </div>
            <Row className={"mt-3"}>
              <Container>
                <Button
                  className="text-center mr-3"
                  variant="primary"
                  onClick={this.props.addFilterBtnOnClick}
                >
                  Add Filter
                </Button>
                <Button
                  className="text-center"
                  variant="success"
                  onClick={this.props.searchBtnOnClick}
                >
                  Search
                </Button>
              </Container>
            </Row>
          </Form.Group>
        </Form>
      </Jumbotron>
    )
  }
}


class TextInputWithUnits extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    const inputWidth = this.props.inputWidth ? this.props.inputWidth : "90%";
    return (
      <div>
        {/*<Form>*/}
        <h6>
          {ReactHtmlParser(this.props.label)}
        </h6>
        <InputGroup
          className="mb-3 input-group-sm"
          style={{width: inputWidth}}>
          <Form.Control
            required={this.props.required ? true : false}
            param={this.props.param}
            ui_percentage={this.props.ui_percentage}
            placeholder={this.props.placeholder}
            defaultValue={this.props.defaultValue}
            onChange={this.props.onChange}
          >
          </Form.Control>
          <InputGroup.Append>
            <InputGroup.Text>
              {ReactHtmlParser(this.props.units)}
            </InputGroup.Text>
          </InputGroup.Append>
          <Form.Control.Feedback type="invalid">
            *Required
          </Form.Control.Feedback>
        </InputGroup>
        {/*</Form>*/}
      </div>
    )
  }
}

class TextInput extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <Card.Title>
          {this.props.label}
        </Card.Title>
        <InputGroup className="mb-3" style={{width: "70%"}}>
          <Form.Control
            placeholder={this.props.placeholder}>
            onChange={this.props.onChange}
          </Form.Control>
          <Form.Control.Feedback type="invalid">
            *Required
          </Form.Control.Feedback>
        </InputGroup>
      </div>
    )
  }
}

class PropFilter extends React.Component {
  constructor(props) {
    super(props)
  }


  render() {
    return (
      <Row>
        <Col xs={3}>
          <Form.Label className="mr-1">
            <strong>Filter By</strong>
          </Form.Label>
          <Form.Control
            required
            as="select"
            size="md"
            style={{width: 190}}
            id={this.props.id}
            onChange={this.props.filterPropSelectOnChange}
          >
            <option value='mp'>Melting Point (°C)</option>
            <option value='bp'>Boiling Point (°C)</option>
            <option value='fp'>Flash Point (°C)</option>
            <option value='ysi'>Yield Sooting Index</option>
            <option value='cn'>Cetane Number</option>
            {/*<option value='dcn'>Derived Cetane Number</option>*/}
          </Form.Control>
        </Col>
        <Col xs={2}>
          <Form.Label className="mr-1">
            <strong>
              Minimum Value
            </strong>
          </Form.Label>
          <NumericInput
            id={this.props.id}
            onChange={this.props.filterMinValOnChange}
            onKeyUp={this.props.enterOnKeyUp}
            searchBtnOnClick={this.props.searchBtnOnClick}
          />
        </Col>
        <Col xs={2}>
          <Form.Label>
            <strong>
              Maximum Value
            </strong>
          </Form.Label>
          <NumericInput
            id={this.props.id}
            onChange={this.props.filterMaxValOnChange}
            onKeyUp={this.props.enterOnKeyUp}
            searchBtnOnClick={this.props.searchBtnOnClick}
          />
        </Col>
        <Col xs={3}>
          {/*<ToolTipCheckbox>*/}
          {/*</ToolTipCheckbox>*/}
          <strong>
            <Form.Check
              id={this.props.id}
              // className={"mr-1"}
              defaultChecked
              type="checkbox"
              label="Include Predictions"
              style={{position: 'absolute', bottom: 5}}
              onChange={this.props.allowPredValsCheckboxOnChange}
            />
          </strong>
        </Col>
        <Col xs={2}>
          <Button
            className="text-center"
            id={this.props.id}
            variant="danger"
            onClick={this.props.removeFilterBtnOnClick}
            style={
              {
                position: 'absolute',
                bottom: 0,
                display:
                  this.props.removeFilterBtnDisplay ?
                    this.props.removeFilterBtnDisplay
                    : 'block'
              }
            }
          >
            Remove Filter
          </Button>
        </Col>
      </Row>
    )
  }
}

class NumericInput extends React.Component {
  /*
  Reference:
  https://stackoverflow.com/questions/43687964/only-numbers-input-number-in-react
   */
  // onKeyPress(event) {
  //   const keyCode = event.keyCode || event.which;
  //   const keyValue = String.fromCharCode(keyCode);
  //   if (/\+|-/.test(keyValue))
  //     event.preventDefault();
  // }

  render() {
    return (
      <Form.Control
        id={this.props.id}
        style={{width: 120}}
        type="number"
        // onKeyPress={this.onKeyPress.bind(this)}
        onKeyUp={this.props.onKeyUp}
        onChange={this.props.onChange}
      />

    )
  }
}


// ========================================
// Helper functions
// ========================================
const numWithCommas = function (x, d = 0) {
  return parseFloat(x).toFixed(d).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const numWithCommasUSD = function (x, d = 2) {
  return '$' + numWithCommas(parseFloat(x).toFixed(d), d)
}
// ========================================

//
// export default App;
//
// const container = document.getElementById("app");
// ReactDOM.render(
//
{/*<App/>*/
}
//   ,
//   container
// );


ReactDOM.render(
  // gets the props that are passed in the template
  React.createElement(ChemicalSearchPageApp, window.props),
  // a reference to the #react div that we render to
  window.react_mount,
)
