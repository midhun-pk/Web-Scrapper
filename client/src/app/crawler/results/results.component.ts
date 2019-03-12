import { Component, OnInit } from '@angular/core';
import { DataService } from '../shared/data.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {
  results: any;

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getResults().subscribe(results => this.results = results)
  }

}
