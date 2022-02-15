import Rating from '@mui/material/Rating';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import CircularProgress from '@mui/material/CircularProgress';
import InfoIcon from '@mui/icons-material/Info';
import { Component } from 'react';

class FilmRate extends Component {
    constructor(props) {
        super(props);
        this.evaluateComment = this.evaluateComment.bind(this);

        this.state = {
          review: "이 영화 진짜 존잼이다 하하하하핳",
          showModelId: 0,
          movieRates: [
              {
                  modelId: 1,
                  modelName: "Model 01",
                  rate: 0.0,
                  isLoading: false,
              },
              {
                  modelId: 2,
                  modelName: "Model 02",
                  rate: 0.0,
                  isLoading: false,
              },
              {
                  modelId: 3,
                  modelName: "Model 03",
                  rate: 0.0,
                  isLoading: false,
              },
              {
                  modelId: 4,
                  modelName: "Model 04",
                  rate: 0.0,
                  isLoading: false,
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
        {
            let _movieRates = [...this.state.movieRates];
            _movieRates.forEach((movieRate) => {
                if (movieRate.modelId === modelId) {
                    movieRate.isLoading = true;
                }
            });

            this.setState({
                movieRates: _movieRates,
            })
        }

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
                    movieRate.isLoading = false;
                });

                this.setState({
                    movieRates: _movieRates,
                })
            }
        })
    }

    showModelInfo(modelId) {
        this.setState({
            showModelId: modelId,
        })
    }
    closeModelInfo() {
        this.setState({
            showModelId: 0,
        })
    }

    handleKeyPress = (e) => {
        this.closeModelInfo();
    }

    render() {
        return (
            <div class="component">
                {
                    this.state.showModelId > 0 ?
                    <div class="popup" onKeyPress={this.handleKeyPress}>
                        <div class="popupCloseButton">
                            <Button variant="outlined" size="small" 
                                onClick={() => this.closeModelInfo()}>
                                Close
                            </Button>
                        </div>
                    </div>
                    :
                    ""
                }
                <div class="section">
                    <TextField multiline size="small" label="Review" fontWeight="{500}"
                    sx={{ minWidth:450, maxWidth: 450, minHeight:10 }}
                    inputProps={{style: {fontFamily: ['Malgun Gothic'], fontSize: 13, heigth: 22}}}
                    name="review" value={this.state.review} onChange={this.handleChange}>
                    </TextField>
                </div>

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
                        {this.state.movieRates.map(({modelId, modelName, rate, isLoading}) => (
                            <TableRow key={modelId}>
                                <TableCell>
                                    {modelName} 
                                    <InfoIcon onClick={() => this.showModelInfo(modelId)} 
                                        sx={{ fontSize: 15, marginLeft: 1, color: 'darkblue', cursor: 'Pointer' }}>
                                    </InfoIcon>
                                </TableCell>
                                <TableCell>
                                    <Rating value={rate} precision={0.5} size={'large'} readOnly></Rating> ({rate})
                                </TableCell>
                                <TableCell>
                                    <Button id={modelId} variant="outlined" size="small"
                                        onClick={() => this.evaluateComment(modelId)}>
                                        {isLoading ? <CircularProgress size={20}></CircularProgress> : "Start"}
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