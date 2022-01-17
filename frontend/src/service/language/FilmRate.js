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
import { Component } from 'react';

class FilmRate extends Component {
    state = {
        review: "이 영화 진짜 존잼이다 하하하하핳",
        rate: 0.0,
        progress: 0,
    }
    constructor(props) {
        super(props);
        //this.handleChange = this.handleChange.bind(this);
        this.evaluateComment = this.evaluateComment.bind(this);
    }
    handleChange = (e) => {
      //console.log(e.target.value);
        this.setState({
            [e.target.name]: e.target.value
        })
    }
    evaluateComment() {
        fetch("http://127.0.0.1:8000/filmrate/predict", {
          method: "POST",
          headers: {
            'Content-type': 'application/json'
        },
          body: JSON.stringify({
            content: this.state.review
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data !== null && data["rate"] !== null) {
            let rate = data["rate"];
            let ratio = rate * 100 / 5;
            console.log(ratio);
            
            this.setState({
              rate: data["rate"],
              progress: ratio
            });
          }
        });
    }

    render() {
        return (
            <div class="component">
                {/* <form> */}
                    <div class="section">
                      {/* <textarea name="review" class="content" value={this.state.review} onChange={this.handleChange}></textarea> */}
                      {/* <input
                          class="content"
                          value={this.state.review}
                          onChange={this.handleChange}
                          name="review"
                      /> */}
                      {/* <div>{this.state.review}</div> */}
                      <TextField multiline size="small" label="Review" fontWeight="{500}"
                        sx={{ minWidth:700, maxWidth: 750, minHeight:10 }}
                        inputProps={{style: {fontFamily: ['Malgun Gothic'], fontSize: 13, heigth: 22}}}
                        name="review" value={this.state.review} onChange={this.handleChange}>
                      </TextField>
                      <div class="inline">
                        <Button variant="contained" endIcon={<SendIcon />} 
                          size="middle"
                          onClick={this.evaluateComment}>Eval</Button>
                      </div>
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
                            {/* <TableCell align="right">Calories</TableCell> */}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          <TableRow>
                            <TableCell>Basic</TableCell>
                            <TableCell>
                              <Rating value={this.state.rate} precision={0.5} size={'large'} readOnly></Rating> ({this.state.rate})
                            </TableCell>
                          </TableRow>
                          {/* {rows.map((row) => (
                            <TableRow
                              key={row.name}
                              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                              <TableCell component="th" scope="row">
                                {row.name}
                              </TableCell>
                              <TableCell align="right">{row.calories}</TableCell>
                              <TableCell align="right">{row.fat}</TableCell>
                              <TableCell align="right">{row.carbs}</TableCell>
                              <TableCell align="right">{row.protein}</TableCell>
                            </TableRow>
                          ))} */}
                        </TableBody>
                      </Table>
                    </TableContainer>
                    </div>
                {/* </form> */}
            </div>
        );
    }
  }

  export default FilmRate;