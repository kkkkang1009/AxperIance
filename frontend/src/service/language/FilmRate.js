import Rating from '@mui/material/Rating';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import SendIcon from '@mui/icons-material/Send';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import PropTypes from 'prop-types';
import { Component } from 'react';

class FilmRate extends Component {
    // static MovieRate = {
    //     modelName: PropTypes.string.isRequired,
    //     rate: PropTypes.number.isRequired,
    // };

    constructor(props) {
        super(props);
        this.evaluateComment = this.evaluateComment.bind(this);

        this.state = {
          review: "이 영화 진짜 존잼이다 하하하하핳",
          movieRates: [
              {
                  modelId: 1,
                  modelName: "Model 01",
                  rate: 0.0,
              },
              {
                  modelId: 2,
                  modelName: "Model 02",
                  rate: 0.0,
              },
              {
                  modelId: 3,
                  modelName: "Model 03",
                  rate: 0.0,
              }
          ]
        };
    }
    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }
    evaluateComment(modelId) {
        fetch("http://127.0.0.1:8000/filmrate/predict", {
          method: "POST",
          headers: {
            'Content-type': 'application/json'
        },
          body: JSON.stringify({
            modelId: modelId,
            content: this.state.review
          })
        })
        .then(response => response.json())
        .then(jsonRes => jsonRes["result"])
        .then(result => {
            if (result != null) {
                const modelId = result["modelId"];
                const rate = result["rate"];

                let _movieRates = [...this.state.movieRates];
                _movieRates.forEach((movieRate) => {
                    if (movieRate.modelId === modelId) {
                        movieRate.rate = rate;
                    }
                });

                this.setState({
                    movieRates: _movieRates
                })
            }
        })
    }

    render() {
        return (
            <div class="component">
                <div class="section">
                    <TextField multiline size="small" label="Review" fontWeight="{500}"
                    sx={{ minWidth:700, maxWidth: 750, minHeight:10 }}
                    inputProps={{style: {fontFamily: ['Malgun Gothic'], fontSize: 13, heigth: 22}}}
                    name="review" value={this.state.review} onChange={this.handleChange}>
                    </TextField>
                    {/* <div class="inline">
                        <Button variant="contained" endIcon={<SendIcon />} 
                            size="middle"
                            onClick={this.evaluateComment}>Eval</Button>
                    </div> */}
                </div>

                {/* <div class="section">
                    <div>Expected Rate : {this.state.rate}</div>
                    <div className="progress-div">
                        <div style={{width: `${this.state.progress}%`}} className="progress"/>
                    </div>
                    <Rating value={this.state.rate} precision={0.5} size={'large'} readOnly></Rating>
                </div> */}
                <div class="section">
                <TableContainer component={Paper} sx={{ minWidth: 350, maxWidth:700 }}>
                    <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                        <TableCell>Model</TableCell>
                        <TableCell>Expected Rate</TableCell>
                        <TableCell>Evaluate</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.state.movieRates.map(({modelId, modelName, rate}) => (
                            <TableRow key={modelId}>
                                <TableCell>{modelName}</TableCell>
                                <TableCell>
                                    <Rating value={rate} precision={0.5} size={'large'} readOnly></Rating> ({rate})
                                </TableCell>
                                <TableCell>
                                    <Button id={modelId} variant="contained" endIcon={<SendIcon />} size="middle" onClick={() => this.evaluateComment(modelId)}>
                                        Start
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                    </Table>
                </TableContainer>
                </div>
            </div>
        );
    }
  }

  export default FilmRate;