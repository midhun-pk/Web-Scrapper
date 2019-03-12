import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { DataService } from '../shared/data.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  isValid = true;
  crawling: Boolean;

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getStatus().subscribe(status => this.crawling = status);
  }

  onSubmit(crawlerForm: NgForm) {
    const depth: Number = crawlerForm.form.value['depth'];
    const url: String = crawlerForm.form.value['url'];
    if (depth > 0 && crawlerForm.form.valid) {
      this.isValid = true;
      this.dataService.setResults([]);
      this.dataService.crawl(url, depth);
    } else {
      this.isValid = false;
    }
  }

}
