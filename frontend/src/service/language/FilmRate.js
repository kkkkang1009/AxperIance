import Tab from '@mui/material/Tab';
import { Component } from 'react';

class FilmRate extends Component {
    state = {
        review: '',
        rate: 0.0,
    }
    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }
    render() {
        return (
            <div class="component">
                <form>
                    <div class="section">
                        <input
                            class="content"
                            value={this.state.review}
                            onChange={this.handleChange}
                            name="review"
                        />
                        {/* <div>{this.state.review}</div> */}
                        <div>
                            <button>Evaluate</button>
                        </div>
                    </div>

                    <div class="section">
                        <div>Expected Rate : {this.state.rate}</div>
                    </div>
                </form>
            </div>
        );
    }
  }

  export default FilmRate;