import Tab from '@mui/material/Tab';
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
                        <input
                            class="content"
                            value={this.state.review}
                            onChange={this.handleChange}
                            name="review"
                        />
                        {/* <div>{this.state.review}</div> */}
                        <div>
                            <button onClick={this.evaluateComment}>Evaluate</button>
                        </div>
                    </div>

                    <div class="section">
                        <div>Expected Rate : {this.state.rate}</div>
                        <div className="progress-div">
                          <div style={{width: `${this.state.progress}%`}} className="progress"/>
                        </div>
                    </div>
                {/* </form> */}
            </div>
        );
    }
  }

  export default FilmRate;