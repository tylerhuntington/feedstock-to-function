import React from 'react';
import ReactDOM from 'react-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Popover from 'react-bootstrap/Popover'
import Jumbotron from 'react-bootstrap/Jumbotron';
import InputGroup from 'react-bootstrap/InputGroup';
import ReactHtmlParser from 'react-html-parser';
import axios from 'axios';
import Parser from 'html-react-parser'
import {Bars} from 'svg-loaders-react'

import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
// import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
// import getMuiTheme from 'material-ui/lib/getMuiTheme';
// import MuiThemeProvider from 'material-ui/lib/MuiThemeProvider';
import {createMuiTheme} from '@material-ui/core/styles';
import {ThemeProvider} from '@material-ui/styles';
import blendData from './blend_data.json'
// import blendData from 'json!./blendData.json';


const theme = createMuiTheme({
  overrides: {
    MuiSlider: {
      thumb: {
        color: "#28a745",
      },
      track: {
        color: "#28a745",
      },
      rail: {
        color: "#28a745",
      }
    }
  }
});
const jetFuelSliderTheme = createMuiTheme({
  overrides: {
    MuiSlider: {
      thumb: {
        color: "#0062cc",
      },
      track: {
        color: '#0062cc'
      },
      rail: {
        color: '#0062cc'
      }
    }
  }
});


// const muiTheme = getMuiTheme({
//   slider: {
//     trackColor: "yellow",
//     selectionColor: "red"
//   }
// });


const additiveRangeMarks = [
  {
    value: 0,
    label: '0%',
  },
  {
    value: 5,
    label: '5%',
  },
  {
    value: 10,
    label: '10%',
  },
  {
    value: 15,
    label: '15%',
  },
  {
    value: 20,
    label: '20%',
  },
  {
    value: 25,
    label: '25%',
  },
  {
    value: 30,
    label: '30%',
  },
];

const jetFuelRangeMarks = [
  {
    value: 70,
    label: '70%',
  },
  {
    value: 75,
    label: '75%',
  },
  {
    value: 80,
    label: '80%',
  },
  {
    value: 85,
    label: '85%',
  },
  {
    value: 90,
    label: '90%',
  },
  {
    value: 95,
    label: '95%',
  },
  {
    value: 100,
    label: '100%',
  },
];

const additiveAliases = {
  "Farnesane":
    "farnesane",
  "Pinane":
    "pinane",
  "P-menthane":
    "pmenthane",
  "RJ-4":
    "rj"
}

const jetFuelAliases = {
  "Jet A":
    "jeta"
}


function valuetext(value) {
  return `${value}%`;
}


class ChemicalBlendPageApp extends React.Component {
  constructor(props) {
    const defaultJetFuel = 'Jet A';
    const defaultAdditive = 'Farnesane';
    const defaultAdditivePerc = 20;
    const defaultJetFuelPerc = 80;
    super(props)
    this.state = {
      selectedJetFuel: defaultJetFuel,
      selectedAdditive: defaultAdditive,
      additivePerc: defaultAdditivePerc,
      jetFuelPerc: defaultJetFuelPerc,
      resultsSectionDisplay: 'block',
      searchSpinnerDisplay: 'none',
      mp: 126,
      bp: 367,
      fp: 435,
      cn: 79,
      ysi: 194,
    }
    // Bind event handlers.
    this.jetFuelSelectOnChange = this.jetFuelSelectOnChange.bind(this)
    this.additiveSelectOnChange = this.additiveSelectOnChange.bind(this)
    this.additiveRangeOnChange = this.additiveRangeOnChange.bind(this)
    this.jetFuelRangeOnChange = this.jetFuelRangeOnChange.bind(this)

  };

  // Define event handlers.
  jetFuelSelectOnChange(event) {
    this.setState({
        selectedJetFuel: event.target.value
      }
    )
  }

  additiveSelectOnChange(event) {
    this.setState({
        selectedAdditive: event.target.value
      }
    )
  }

  additiveRangeOnChange(event, value) {
    this.setState({
        additivePerc: parseFloat(value),
        jetFuelPerc: 100 - value,
      }
    )
  }

  jetFuelRangeOnChange(event, value) {
    this.setState({
        jetFuelPerc: parseFloat(value),
        additivePerc: 100 - value,
      }
    )
  }

  render() {
    return (
      <ThemeProvider theme={theme}>
        <Container>
          <br></br>
          {/*<h2>Design Blend</h2>*/}
          <Jumbotron style={{padding: "2% 3%", textAlign: 'center'}}>
            <h3 >
            Blend Tool Coming Soon!
            </h3>
          </Jumbotron>
        </Container>
        {/*<Container>*/}
        {/*  <BlendInputsJumbo*/}
        {/*    selectedAdditive={this.state.selectedAdditive}*/}
        {/*    selectedJetFuel={this.state.selectedJetFuel}*/}
        {/*    jetFuelPerc={this.state.jetFuelPerc}*/}
        {/*    additivePerc={this.state.additivePerc}*/}
        {/*    jetFuelSelectOnChange={this.jetFuelSelectOnChange}*/}
        {/*    additiveSelectOnChange={this.additiveSelectOnChange}*/}
        {/*    additiveRangeOnChange={this.additiveRangeOnChange}*/}
        {/*    jetFuelRangeOnChange={this.jetFuelRangeOnChange}*/}
        {/*  />*/}
        {/*  <BlendResults*/}
        {/*    display={this.state.resultsSectionDisplay}*/}
        {/*    jetFuelPerc={this.state.jetFuelPerc}*/}
        {/*    additivePerc={this.state.additivePerc}*/}
        {/*    selectedAdditive={this.state.selectedAdditive}*/}
        {/*    selectedJetFuel={this.state.selectedJetFuel}*/}
        {/*    bp={this.state.bp}*/}
        {/*    mp={this.state.mp}*/}
        {/*    fp={this.state.fp}*/}
        {/*    cn={this.state.cn}*/}
        {/*    ysi={this.state.ysi}*/}
        {/*    // blendProps={this.state.blendProps}*/}
        {/*    // additiveProps={this.state.additiveProps}*/}
        {/*    // jetFuelProps={this.state.jetFuelProps}*/}
        {/*  />*/}
        {/*</Container>*/}
      </ThemeProvider>
    );
  }
}

class BlendResults extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    const jetFuel = jetFuelAliases[this.props.selectedJetFuel]
    const additive = additiveAliases[this.props.selectedAdditive]
    const additiveKey = `${additive}_100`
    const jetFuelKey = `${jetFuel}_100`
    var blendKey
    if (this.props.jetFuelPerc === 100) {
      blendKey = jetFuelKey;
    } else if (this.props.additivePerc === 100) {
      blendKey = additiveKey;
    } else {
      blendKey = (
        `${additive}${this.props.additivePerc}_`
        + `${jetFuel}${this.props.jetFuelPerc}`
      )
    }

    var blendProps = nullToString(blendData[blendKey], '-')
    blendProps = concatBlendPredsErrs(blendProps)

    var additiveProps = nullToString(blendData[additiveKey], '-')
    additiveProps = concatBlendPredsErrs(additiveProps)

    var jetFuelProps = nullToString(blendData[jetFuelKey], '-')
    jetFuelProps = concatBlendPredsErrs(jetFuelProps)

    console.log(blendData)

    return (
      <div>
        <Card
          key={`${this.props.selectedJetFuel}_${this.props.selectedAdditive}`}>
          <Card.Header as="h5" className={'text-center'}>
            Blend & Component Properties</Card.Header>
          <Card.Body>
            <Table striped bordered hover className={'text-center'}>
              <thead>
              <tr>
                <th></th>
                <td colSpan={2} className={"text-center"}
                    style=
                      {{
                        backgroundColor: '#FF671130',
                        fontStyle: 'italic',
                        borderRight: '3px solid #dee2e6'
                      }}>
                  Blend
                </td>
                <td colSpan={2} className={"text-center"}
                    style={{backgroundColor: '#0062cc30', fontStyle: 'italic'}}>
                  {this.props.selectedJetFuel}
                </td>
                <td colSpan={2} className={"text-center"}
                    style={{backgroundColor: '#28a74530', fontStyle: 'italic'}}>
                  {this.props.selectedAdditive}
                </td>
              </tr>
              <tr>
                <th>Property</th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#FF671130'}}>
                >Experimental
                </th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#FF671130'}}
                    style={{
                      borderRight: '3px solid #dee2e6'
                    }}
                >Predicted
                </th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#0062cc30'}}
                >Experimental
                </th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#0062cc30'}}
                    style={{
                      borderRight: '3px solid #dee2e6'
                    }}
                >Predicted
                </th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#28a74530'}}
                >Experimental
                </th>
                <th className={'text-center'}
                  // style={{backgroundColor: '#28a74530'}}
                >Predicted
                </th>
              </tr>
              </thead>
              <tbody>
              <tr className={'text-center'}>
                <td>Boiling Point (°C)</td>
                <td>{blendProps['bp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{blendProps['bp_c_predicted']}</td>
                <td>{jetFuelProps['bp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >
                  {jetFuelProps['bp_c_predicted']}</td>
                <td>{additiveProps['bp_c_experimental']}</td>
                <td>{additiveProps['bp_c_predicted']}</td>
              </tr>
              <tr>
                <td>Melting Point (°C)</td>
                <td>{blendProps['mp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{blendProps['bp_c_predicted']}</td>
                <td>{jetFuelProps['mp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{jetFuelProps['mp_c_predicted']}</td>
                <td>{additiveProps['mp_c_experimental']}</td>
                <td>{additiveProps['mp_c_predicted']}</td>
              </tr>
              <tr>
                <td>Flash Point (°C)</td>
                <td>{blendProps['fp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{blendProps['fp_c_predicted']}</td>
                <td>{jetFuelProps['fp_c_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{jetFuelProps['fp_c_predicted']}</td>
                <td>{additiveProps['fp_c_experimental']}</td>
                <td>{additiveProps['fp_c_predicted']}</td>
              </tr>
              <tr>
                <td>Cetane Number</td>
                <td>{blendProps['cn_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{blendProps['cn_predicted']}</td>
                <td>{jetFuelProps['cn_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{jetFuelProps['cn_predicted']}</td>
                <td>{additiveProps['cn_experimental']}</td>
                <td>{additiveProps['cn_predicted']}</td>
              </tr>
              <tr>
                <td>Yield Sooting Index</td>
                <td>{blendProps['ysi_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{blendProps['ysi_predicted']}</td>
                <td>{jetFuelProps['ysi_experimental']}</td>
                <td
                  style={{
                    borderRight: '3px solid #dee2e6'
                  }}
                >{jetFuelProps['ysi_predicted']}</td>
                <td>{additiveProps['ysi_experimental']}</td>
                <td>{additiveProps['ysi_predicted']}</td>
              </tr>
              </tbody>
            </Table> </Card.Body>
        </Card></div>
    )
  }
}


class BlendInputsJumbo extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {

    return (
      <div>
        <h3 className={'text-center'}>Explore Blends</h3>
        <h5 className={'text-center'}><strong>
          (Under Development: Do not use this data)
        </strong></h5>
        <Jumbotron style={{padding: "2% 3%"}}>
          <Row>
            <p>
              Our bio-jet fuel blend property prediction
              tool predicts key properties of select high-potential
              bio-based molecules combined with Jet A (F-24) fuel, using
              open-source, Python-based, supervised machine learning packages.
              The models correlate each blend's ATR-FTIR spectroscopy data with
              its corresponding fuel properties: flash point, freezing point,
              cetane number.
            </p>
          </Row>
          <Row>
            <Col>
              {/* Jet Fuel Input */}
              <Form.Group>
                <Form.Label className="mr-1">
                  <strong>Jet Fuel</strong>
                </Form.Label>
                <Form.Control
                  required
                  as="select"
                  size="md"
                  style={{width: 210}}
                  defaultValue={this.props.selectedJetFuel}
                  onChange={this.props.jetFuelSelectOnChange}
                >
                  <option value={'jeta'}>Jet A</option>
                </Form.Control>
              </Form.Group>
            </Col>
            <Col>
              {/* Bio-based Additive Input */}
              <Form.Group>
                <Form.Label className="mr-1">
                  <strong>Bio-based Additive</strong>
                </Form.Label>
                <Form.Control
                  required
                  as="select"
                  size="md"
                  style={{width: 210}}
                  defaultValue={this.props.selectedAdditive}
                  onChange={this.props.additiveSelectOnChange}
                >
                  <option>Farnesane</option>
                  <option>Pinane</option>
                  <option>P-menthane</option>
                  <option>RJ-4</option>
                </Form.Control>
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col>
              {/* Jet Fuel Range slider */}
              <div className='slider' style={{width: 300, margin: 3}}>
                <Typography id="discrete-slider" gutterBottom>
                  <Form.Label className="mr-1">
                    <strong>Percent Volume</strong>
                  </Form.Label>
                </Typography>
                <ThemeProvider theme={jetFuelSliderTheme}>
                  <Slider
                    // defaultValue={this.props.jetFuelPerc}
                    value={this.props.jetFuelPerc}
                    aria-labelledby="discrete-slider"
                    valueLabelDisplay="auto"
                    step={5}
                    marks={jetFuelRangeMarks}
                    getAriaValueText={valuetext}
                    min={70}
                    max={100}
                    onChange={this.props.jetFuelRangeOnChange}
                  />
                </ThemeProvider>
              </div>

            </Col>
            <Col>
              {/* Additive Range slider */}
              <div className='slider' style={{width: 300, margin: 3}}>
                <Typography id="discrete-slider" gutterBottom>
                  <Form.Label className="mr-1">
                    <strong>Percent Volume</strong>
                  </Form.Label>
                </Typography>
                <Slider
                  // defaultValue={this.props.additivePerc}
                  value={this.props.additivePerc}
                  aria-labelledby="discrete-slider"
                  valueLabelDisplay="auto"
                  step={5}
                  marks={additiveRangeMarks}
                  min={0}
                  max={30}
                  onChange={this.props.additiveRangeOnChange}
                />
              </div>
            </Col>
          </Row>
          {/*        <Form.Label className="mr-1">*/}
          {/*          <strong>Search Term</strong>*/}
          {/*        </Form.Label>*/}
          {/*        <Form.Control*/}
          {/*          style={{width: 250}}*/}
          {/*          onChange={this.props.searchTermOnChange}*/}
          {/*          defaultValue={''}*/}
          {/*          onKeyUp={this.props.enterOnKeyUp}*/}
          {/*        />*/}
          {/*        <Popover id="popover-basic"*/}
          {/*                 placement={'right'}*/}
          {/*                 show={false}*/}
          {/*                 style={{*/}
          {/*                   'marginLeft': 280,*/}
          {/*                   'marginTop': 30,*/}
          {/*                   'display': this.props.searchTermReqPopDisplay*/}
          {/*                   // 'display': 'none'*/}
          {/*                 }}*/}
          {/*        >*/}
          {/*          <Popover.Content>*/}
          {/*            <strong>Search Term Required</strong>*/}
          {/*          </Popover.Content>*/}
          {/*        </Popover>*/}
          {/*      </Col>*/}
          {/*    </Row>*/}
          {/*  </Form.Group>*/}
          {/*  <Form.Group>*/}
          {/*    <div style={{display: this.props.propFilters[1]['display']}}>*/}
          {/*      <PropFilter*/}
          {/*        id={1}*/}
          {/*        removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}*/}
          {/*        filterPropSelectOnChange={this.props.filterPropSelectOnChange}*/}
          {/*        filterMinValOnChange={this.props.filterMinValOnChange}*/}
          {/*        filterMaxValOnChange={this.props.filterMaxValOnChange}*/}
          {/*        allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}*/}
          {/*        enterOnKeyUp={this.props.enterOnKeyUp}*/}
          {/*      />*/}
          {/*    </div>*/}
          {/*    <div style={{display: this.props.propFilters[2]['display']}}>*/}
          {/*      <PropFilter*/}
          {/*        id={2}*/}
          {/*        removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}*/}
          {/*        filterPropSelectOnChange={this.props.filterPropSelectOnChange}*/}
          {/*        filterMinValOnChange={this.props.filterMinValOnChange}*/}
          {/*        filterMaxValOnChange={this.props.filterMaxValOnChange}*/}
          {/*        allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}*/}
          {/*        enterOnKeyUp={this.props.enterOnKeyUp}*/}
          {/*      />*/}
          {/*    </div>*/}
          {/*    <div style={{display: this.props.propFilters[3]['display']}}>*/}
          {/*      <PropFilter*/}
          {/*        id={3}*/}
          {/*        removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}*/}
          {/*        filterPropSelectOnChange={this.props.filterPropSelectOnChange}*/}
          {/*        filterMinValOnChange={this.props.filterMinValOnChange}*/}
          {/*        filterMaxValOnChange={this.props.filterMaxValOnChange}*/}
          {/*        allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}*/}
          {/*        enterOnKeyUp={this.props.enterOnKeyUp}*/}
          {/*      />*/}
          {/*    </div>*/}
          {/*    <div style={{display: this.props.propFilters[4]['display']}}>*/}
          {/*      <PropFilter*/}
          {/*        id={4}*/}
          {/*        removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}*/}
          {/*        filterPropSelectOnChange={this.props.filterPropSelectOnChange}*/}
          {/*        filterMinValOnChange={this.props.filterMinValOnChange}*/}
          {/*        filterMaxValOnChange={this.props.filterMaxValOnChange}*/}
          {/*        allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}*/}
          {/*        enterOnKeyUp={this.props.enterOnKeyUp}*/}
          {/*      />*/}
          {/*    </div>*/}
          {/*    <div style={{display: this.props.propFilters[5]['display']}}>*/}
          {/*      <PropFilter*/}
          {/*        id={5}*/}
          {/*        removeFilterBtnOnClick={this.props.removeFilterBtnOnClick}*/}
          {/*        filterPropSelectOnChange={this.props.filterPropSelectOnChange}*/}
          {/*        filterMinValOnChange={this.props.filterMinValOnChange}*/}
          {/*        filterMaxValOnChange={this.props.filterMaxValOnChange}*/}
          {/*        allowPredValsCheckboxOnChange={this.props.allowPredValsCheckboxOnChange}*/}
          {/*        searchBtnOnClick={this.props.searchBtnOnClick}*/}
          {/*        enterOnKeyUp={this.props.enterOnKeyUp}*/}
          {/*      />*/}
          {/*    </div>*/}
          {/*    <Row className={"mt-3"}>*/}
          {/*      <Container>*/}
          {/*        <Button*/}
          {/*          className="text-center mr-3"*/}
          {/*          variant="primary"*/}
          {/*          onClick={this.props.addFilterBtnOnClick}*/}
          {/*        >*/}
          {/*          Add Filter*/}
          {/*        </Button>*/}
          {/*        <Button*/}
          {/*          className="text-center"*/}
          {/*          variant="success"*/}
          {/*          onClick={this.props.searchBtnOnClick}*/}
          {/*        >*/}
          {/*          Search*/}
          {/*        </Button>*/}
          {/*      </Container>*/}
          {/*    </Row>*/}
          {/*  </Form.Group>*/}
          {/*</Form>*/}
        </Jumbotron>
      </div>
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

const nullToString = function (obj, string_val) {

  function recursiveFix(o) {
    // loop through each property in the provided value
    for (var k in o) {
      // make sure the value owns the key
      if (o.hasOwnProperty(k)) {
        if (o[k] === null) {
          // if the value is null, set it to 'null'
          o[k] = string_val;
        } else if (typeof (o[k]) !== 'string' && o[k].length > 0) {
          // if there are sub-keys, make a recursive call
          recursiveFix(o[k]);
        }
      }
    }
  }

  var cloned = jQuery.extend(true, {}, obj)
  recursiveFix(cloned);
  return cloned;
}

const concatBlendPredsErrs = function (obj) {

  const props = ['fp_c', 'mp_c', 'bp_c', 'cn', 'ysi']
  for (let i in props) {
    const pred_key = `${props[i]}_predicted`
    const err_key = `${props[i]}_uncertainty`
    const pred_val = obj[pred_key]
    const err_val = obj[err_key]
    if (pred_val !== '-' && err_val !== '-') {
      obj[pred_key] = `${pred_val} ± ${err_val}`
    } else {
      break
    }
  }
  return obj
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
  React.createElement(ChemicalBlendPageApp, window.props),
  // a reference to the #react div that we render to
  window.react_mount,
)
